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
        print(f"\nPlaywright: Scraping quizzes for {course_name} (Index {index})...")
        
        quiz_icon_id = f"MainContent_gvCourseList_ibtnQuizzes_{index}"
        
        try:
            with self.page.expect_navigation(timeout=15000):
                self.page.locator(f"id={quiz_icon_id}").click(timeout=10000)
        except Exception as e:
            print(f"Playwright Error: Could not navigate to quiz page for {course_name}. Skipping.")
            return []
            
        print(f"   -> Navigated to URL: {self.page.url}")
        quizzes = []
        
        # Wait specifically for the quiz table to appear (waiting for the word 'Title' or 'Marks')
        try:
            self.page.wait_for_selector("text='Total Marks'", timeout=5000)
            print("   -> Quiz table header found. Waiting 2 seconds for DOM to settle...")
            self.page.wait_for_timeout(2000) # Hard wait to ensure AJAX/rendering finishes
        except:
            print("   -> Playwright Warning: Quiz table header ('Total Marks') not found within 5s.")
            
        # Extract grid rows using the Repeater Panel IDs
        panels = self.page.locator("div[id*='gvTileRepeaterQuiz_pnl_']").all()
        print(f"   -> Found {len(panels)} quiz panels on this page.")
        
        # If panels are found, process each one individually
        if len(panels) > 0:
            for panel in panels:
                try:
                    text = panel.inner_text().strip()
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    
                    # Find the title index
                    title_idx = -1
                    for i, line in enumerate(lines):
                        text_lower = line.lower()
                        if "quiz" in text_lower and len(text_lower) < 40 and "chrome" not in text_lower:
                            title_idx = i
                            break
                            
                    if title_idx != -1:
                        title = lines[title_idx]
                        start = "N/A"
                        end = "N/A"
                        marks = "0"
                        open_close = "Closed"
                        status = ""
                        result = "0"
                        
                        curr = title_idx + 1
                        if curr < len(lines):
                            start = lines[curr]
                            curr += 1
                        if curr < len(lines):
                            end = lines[curr]
                            curr += 1
                        if curr < len(lines):
                            marks = lines[curr]
                            curr += 1
                        if curr < len(lines):
                            open_close = lines[curr]
                            curr += 1
                        if curr < len(lines):
                            val = lines[curr]
                            # If it's a number, it's the result and status was empty
                            if val.isdigit() or val == "N/A" or val == "-":
                                result = val
                            else:
                                status = val
                                curr += 1
                                if curr < len(lines):
                                    result = lines[curr]
                                    
                        if not any(q['title'] == title for q in quizzes):
                            quizzes.append({
                                "number": len(quizzes) + 1,
                                "title": title,
                                "start": start,
                                "end": end,
                                "totalMarks": marks,
                                "open_close": open_close,
                                "status": status,
                                "result": result
                            })
                            print(f"   -> ✅ Extracted: {title} | Status: {status}")
                except Exception as e:
                    print(f"   -> ❌ Error parsing quiz panel: {e}")
        else:
            # Fallback: Extract all text from the main container and chunk it
            print("   -> No panels found. Attempting fallback full-text parsing...")
            container = self.page.locator(".Accounttbl").last
            if container.count() == 0:
                container = self.page.locator("body")
                
            text = container.inner_text().strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            idx = 0
            while idx < len(lines):
                text_lower = lines[idx].lower()
                if "quiz" in text_lower and len(text_lower) < 40 and "chrome" not in text_lower:
                    try:
                        title = lines[idx]
                        start = lines[idx+1] if idx+1 < len(lines) else ""
                        end = lines[idx+2] if idx+2 < len(lines) else ""
                        marks = lines[idx+3] if idx+3 < len(lines) else "0"
                        open_close = lines[idx+4] if idx+4 < len(lines) else "Closed"
                        status = lines[idx+5] if idx+5 < len(lines) else ""
                        result = lines[idx+6] if idx+6 < len(lines) else "0"
                        
                        if status.isdigit() or status == "N/A" or status == "-":
                            result = status
                            status = ""
                            idx += 6
                        else:
                            idx += 7
                            
                        if not any(q['title'] == title for q in quizzes):
                            quizzes.append({
                                "number": len(quizzes) + 1,
                                "title": title,
                                "start": start,
                                "end": end,
                                "totalMarks": marks,
                                "open_close": open_close,
                                "status": status,
                                "result": result
                            })
                            print(f"   -> ✅ Extracted (Fallback): {title} | Status: {status}")
                    except IndexError:
                        idx += 1
                else:
                    idx += 1
                    
        # Click the Back button to return cleanly
        back_btn = self.page.locator("a:has-text('Back'), a:has-text('◀ Back'), input[value*='Back'], a.back-btn")
        if back_btn.count() > 0:
            try:
                with self.page.expect_navigation(timeout=15000):
                    back_btn.first.click()
            except:
                self.page.goto("https://vulms.vu.edu.pk/home.aspx")
                self.page.wait_for_load_state("networkidle")
        else:
            print("   -> 'Back' button not found, falling back to home.aspx")
            self.page.goto("https://vulms.vu.edu.pk/home.aspx")
            self.page.wait_for_load_state("networkidle")
            
        return quizzes

# Singleton instance ta ke pura project aik hi browser session use kare
browser_service = BrowserService()
