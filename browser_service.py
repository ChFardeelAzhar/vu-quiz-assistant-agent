from playwright.sync_api import sync_playwright

class BrowserService:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start_browser(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            # headless=False rakhne se browser samne open hoga
            self.browser = self.playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()

    def close_browser(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def login_to_vu(self, vu_id, vu_pass):
        print("Playwright: Opening VU LMS...")
        self.page.goto("https://vulms.vu.edu.pk/LMS_LP.aspx")
        
        content = self.page.content()
        if "Student ID" in content or "Password" in content or "Sign In" in content:
            print(f"Playwright: Form found. Logging in as {vu_id}...")
            
            # Playwright ke built-in robust locators
            # get_by_placeholder sab se best tarika hai
            if self.page.get_by_placeholder("Student ID").is_visible():
                self.page.get_by_placeholder("Student ID").fill(vu_id)
            else:
                self.page.locator("input[type='text']").first.fill(vu_id)

            if self.page.get_by_placeholder("Password").is_visible():
                self.page.get_by_placeholder("Password").fill(vu_pass)
            else:
                self.page.locator("input[type='password']").first.fill(vu_pass)
            
            # Sign In button par click
            self.page.get_by_text("Sign In").click()
            
            # Wait for dashboard to load
            self.page.wait_for_load_state("networkidle")
        
        print("Playwright: Logged in! Current Title:", self.page.title())
        return True

    def extract_courses_from_dashboard(self):
        """Scans the DOM for course indices and titles."""
        print("Playwright: Navigating to Dashboard to extract courses...")
        self.page.goto("https://vulms.vu.edu.pk/home.aspx")
        self.page.wait_for_load_state("networkidle")
        
        courses_dict = {}
        # Find all elements matching the id pattern MainContent_gvCourseList_ibtnCourseHome_*
        course_links = self.page.locator("a[id^='MainContent_gvCourseList_ibtnCourseHome_'], input[id^='MainContent_gvCourseList_ibtnCourseHome_']").all()
        
        for link in course_links:
            # Skip if disabled (no active quizzes)
            cls = link.get_attribute("class") or ""
            if "aspNetDisabled" in cls:
                continue
                
            element_id = link.get_attribute("id")
            title = link.get_attribute("title")
            
            if element_id and title:
                # Extract the numeric index from the end of the ID
                # Example ID: MainContent_gvCourseList_ibtnCourseHome_0
                parts = element_id.split("_")
                for part in reversed(parts):
                    if part.isdigit():
                        index_val = int(part)
                        # Agar ye index pehle save nahi hua, to dictionary mein daal do
                        if index_val not in courses_dict:
                            courses_dict[index_val] = title.strip()
                        break
                        
        # Dictionary ko wapis list of dicts mein convert karna ta ke sorted rahay
        courses = [{"index": k, "name": v} for k, v in sorted(courses_dict.items())]
        
        print(f"Playwright: Extracted {len(courses)} unique active courses from Dashboard.")
        return courses

    def scrape_course_quizzes(self, index, course_name):
        """Clicks the quiz icon for the given index, scrapes the table, and clicks back."""
        print(f"Playwright: Scraping quizzes for {course_name} (Index {index})...")
        
        # Click the specific course's Quizzes icon
        quiz_icon_id = f"MainContent_gvCourseList_ibtnQuizzes_{index}"
        
        # Playwright auto-waits for the element to be visible and clickable
        try:
            self.page.locator(f"id={quiz_icon_id}").click(timeout=10000)
            # Wait for postback to complete and quiz table to load
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Playwright Error: Could not click quiz icon for {course_name}. Skipping.")
            return []
            
        quizzes = []
        
        # Extract table rows
        rows = self.page.locator("tr").all()
        for row in rows[1:]: # Skip header
            text = row.inner_text().lower()
            if "quiz #" in text:
                cols = row.locator("td").all()
                if len(cols) >= 7:
                    quiz_title = cols[1].inner_text().strip()
                    start_date = cols[2].inner_text().strip()
                    end_date = cols[3].inner_text().strip()
                    # Screenshot se dekha ja sakta hai ke columns kis tarteeb mein hain
                    total_marks = cols[4].inner_text().strip() if len(cols) > 4 else "0"
                    open_close = cols[5].inner_text().strip() if len(cols) > 5 else "Closed"
                    status = cols[6].inner_text().strip() if len(cols) > 6 else ""
                    result = cols[7].inner_text().strip() if len(cols) > 7 else "0"
                    
                    quizzes.append({
                        "number": len(quizzes) + 1,
                        "title": quiz_title,
                        "start": start_date,
                        "end": end_date,
                        "totalMarks": total_marks,
                        "open_close": open_close,
                        "status": status,
                        "result": result
                    })
                    print(f"   -> Scraped: {quiz_title} | Status: {status}")
                    
        # Click the Back button to return cleanly (maintaining session context)
        # Screenshot mein ek "< Back" button nazar aata hai upper right corner mein
        back_btn = self.page.locator("a:has-text('Back'), a:has-text('◀ Back'), input[value*='Back'], a.back-btn")
        if back_btn.count() > 0:
            back_btn.first.click()
            self.page.wait_for_load_state("networkidle")
        else:
            print("Playwright Warning: 'Back' button not found, falling back to home.aspx")
            self.page.goto("https://vulms.vu.edu.pk/home.aspx")
            self.page.wait_for_load_state("networkidle")
            
        return quizzes

# Singleton instance ta ke pura project aik hi browser session use kare
browser_service = BrowserService()
