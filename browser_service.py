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

    def get_pending_quizzes(self):
        print("Playwright: Navigating to Dashboard...")
        self.page.goto("https://vulms.vu.edu.pk/home.aspx")
        self.page.wait_for_load_state("networkidle")
        
        # 1. Dashboard se tamam Quiz links (hrefs) extract karna
        print("Playwright: Extracting quiz links...")
        quiz_links = set() # Set ta ke duplicate links jama na hon
        elements = self.page.locator("a[href*='QuizList.aspx']").all()
        
        for el in elements:
            href = el.get_attribute("href")
            if href:
                # Agar link relative hai to usey absolute banayen
                full_url = href if href.startswith("http") else f"https://vulms.vu.edu.pk/{href.lstrip('/')}"
                quiz_links.add(full_url)
                
        print(f"Playwright: Found {len(quiz_links)} unique quiz pages.")
        
        pending_quizzes = []
        
        # 2. Har quiz page par jana aur table read karna
        for url in quiz_links:
            print(f"Playwright: Checking quizzes at {url}")
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            
            # Course Title (Subject Name) nikalna
            course_title = "Unknown Course"
            # H1, H2 ya kisi page-title tag se course name uthana
            title_locators = self.page.locator("span[id*='lblCourseName'], h1, h2, .page-title")
            if title_locators.count() > 0:
                course_title = title_locators.first.inner_text().strip()
                
            # Table ki tamam rows nikalna
            rows = self.page.locator("tr").all()
            for row in rows[1:]: # Skip header row
                text = row.inner_text().lower()
                
                if "quiz #" in text:
                    # Columns extract karna (Title, Start Date, End Date, Status)
                    cols = row.locator("td").all()
                    if len(cols) >= 7:
                        quiz_title = cols[1].inner_text().strip()
                        start_date = cols[2].inner_text().strip()
                        end_date = cols[3].inner_text().strip()
                        status = cols[6].inner_text().strip()
                        
                        print(f"   -> [Course: {course_title}] {quiz_title} | Status: {status} | Dates: {start_date} to {end_date}")
                        
                        # Agar closed nahi hai to pending mein daal do
                        if "closed" not in text and "result declared" not in text:
                            print(f"✅ OPEN QUIZ FOUND! Subject: {course_title}")
                            pending_quizzes.append({
                                "subject": course_title,
                                "title": quiz_title,
                                "url": url
                            })
                            
        return pending_quizzes

# Singleton instance ta ke pura project aik hi browser session use kare
browser_service = BrowserService()
