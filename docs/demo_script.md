# ResumeIQ AI: Recruiter Demo Walkthrough Script

This script outlines a 2-3 minute live demonstration flow designed for recruiters and hiring managers.

---

## Part 1: Introduction (0:00 - 0:30)

### Visual Action
* Start on the **Dashboard** page showing the KPI blocks (1,024 candidates, 72.8% Average ATS score) and the Hiring Funnel vertical chart.

### Narration
> "Hello! Today I am demonstrating ResumeIQ AI, an advanced recruiting intelligence platform designed to transform traditional keyword matching into deep semantic searches. 
> 
> Here on the Recruiter Dashboard, we get a bird's-eye view of our talent acquisition pipeline—including candidate counts, average ATS scores, top skills, and funnel distributions. Next, let's look at how we parse individual candidates."

---

## Part 2: Resume Analyzer (0:30 - 1:10)

### Visual Action
* Click on **Resume Analyzer** in the Sidebar.
* Paste in the resume text for Skyler White (Machine Learning Specialist) and click **Analyze Resume**.
* Scroll down to show the predicted ML Engineer title (with confidence), ATS score ring (75%), skill badges, and dynamic learning tracks.

### Narration
> "Under the Resume Analyzer page, a recruiter can paste a candidate's resume or load a text file. When we submit the document, our backend executes multiple NLP and classification steps:
> 
> First, it runs a Logistic Regression classifier to predict the candidate's core category—in this case, identifying Skyler as a Machine Learning Engineer with high confidence. 
> 
> Second, it computes an ATS score breakdown across skills, experience, projects, and education. We can see the extracted skill badges, and the platform dynamically suggests learning tracks for any missing skills."

---

## Part 3: Semantic Job Matching (1:10 - 1:45)

### Visual Action
* Click on **Job Matching** in the Sidebar.
* Paste in Skyler's resume text and click **Find Matching Jobs**.
* Point to the ranked list, highlighting `JOB_011` as Rank 1 and the breakdown of scores.

### Narration
> "But recruiters don't just want score sheets; they need to fit candidates to open roles. If we navigate to Job Matching and paste the same resume, the platform embeds the text into a 384-dimensional dense vector and queries our FAISS index.
> 
> In less than 1 ms, the system retrieves and ranks all active jobs. The best fit is a Machine Learning Engineer position with a 75.7% hybrid matching score, computed combining semantic alignment, ATS scoring, and skill overlap."

---

## Part 4: Candidate Search & Analytics (1:45 - 2:30)

### Visual Action
* Click on **Candidate Search** in the Sidebar.
* Paste a job description for a Software Engineer and click **Search Candidates**. Highlight candidate `CAND_004` at Rank 1.
* Navigate to **Analytics** and show the line, bar, pie, and radar graphs.

### Narration
> "Conversely, hiring managers can perform the reverse search. In Candidate Search, we enter a job description, and the FAISS vector index retrieves the top candidate profiles. 
> 
> Lastly, on our Analytics page, recruiters can track monthly ATS trends, inspect skill frequency distributions, evaluate candidate volume categories, and compare candidates side-by-side using radar overlays. 
> 
> All of these services run inside multi-stage Docker containers with automated Github Actions testing, making ResumeIQ AI a robust, cloud-ready recruiting solution."
