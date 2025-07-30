<p>
  <a href="mailto:robertbostrom4@gmail.com" title="Reach out via email">
    <img src="https://img.shields.io/badge/Ask_me!-anything-orange.svg?style=for-the-badge&logo=gmail" alt="Ask Me Anything" />
  </a>
  &nbsp;&nbsp;
  <img src="https://img.shields.io/github/last-commit/RobertBostrom4/ePortfolio?style=for-the-badge&logo=github" title="ePortfolio Last Update" alt="GitHub Last Commit" />
</p>

<!-- Welcome section -->
## Welcome

This ePortfolio showcases selected projects, assignments, and reflections from my journey through the Computer Science program at Southern New Hampshire University. It highlights my growth in areas such as software engineering, algorithms and data structures, and database development. Each section includes an artifact that demonstrates my abilities in design, implementation, and problem-solving.

<!-- Table of Contents -->
### <u>Table of Contents</u>
- [Professional Self-Assessment](#self-assessment)
- [Refinement Plan and Code Review](#codereview)
- [Software Design and Engineering](#softwaredesign)
- [Algorithms and Data Structures](#algorithms)
- [Databases](#databases)
- [Reviews](#reviews)

<!-- Example Image Embed -->
<img id="self-assessment" src="assets/img/selfassessment.png" alt="Professional Self-Assessment" title="Professional Self-Assessment" />

### _Professional Self-Assessment_

### _Refinement Plan and Code Review_
<div style="text-align: center;">
	<a href="CodeReview" title="Artifacts Code Review">
		<img src="https://img.shields.io/badge/Artifacts-Refinement_Plan and_Code_Review-yellowgreen.svg?style=for-the-badge&logo=codereview" alt="Artifacts: Refinement Plan and Code Review" />
	</a>
</div>

<div style="text-align: right;">
    <a href="#self-assesment">
        <button style="font-size: 10px; font-weight: 500; background: #4169e1; color: #ffffff; border-radius: 50px; border-style: solid; border-color: #4169e1; padding: 5px 5px;">Back to Top &#8593;</button>
    </a>
</div>

<br/>

### _Software Design and Engineering_
The artifact I selected for enhancement was the dashboard from my CS-340 project, which was originally built in a Jupyter Notebook using Python Dash. The dashboard visualized animal rescue data and queried a MongoDB database using a custom CRUD module. Although it was fully functional, the original setup had several limitations that impacted maintainability, security, and potential deployment outside the notebook environment.

To address these concerns, I transformed the notebook into a standalone Python application by refactoring the code into an app.py script. I replaced hardcoded database credentials with environment variables loaded from a .env file, significantly improving the project's security and flexibility. This change also aligned the application more closely with industry standards for configuration management.

Another major enhancement was switching from JupyterDash to dash.Dash, which allowed the app to run as a standalone server, independent of Jupyter. This made the project more modular and deployable in real-world settings. I also set up a secure, locally hosted MongoDB instance with authentication to replace the previous cloud-based setup. All core dashboard functionality, including filters, interactive charts, and map visualizations ,was preserved and fully functional in the new version.

This enhancement clearly aligns with Course Outcome #4, demonstrating the use of well-founded and innovative techniques in computing practices. It also supports Course Outcome #3 by improving the design structure for long-term maintainability and showcasing thoughtful trade-off management in engineering decisions. Overall, I learned how architectural improvements, like removing hardcoded values and isolating configuration , can dramatically improve software quality, security, and readiness for deployment.

### _Algorithms and Data Structures_
The artifact I selected is a Dash-based data dashboard project that connects to a MongoDB database to visualize animal rescue data for the fictional company Grazioso Salvare. I originally created it during CS-340, where we built a full-stack dashboard using Python, Dash, and MongoDB. The project loads animal records from the database and allows users to filter by rescue type, explore breed distribution with a pie chart, and view animal locations on an interactive map.

I chose this artifact for my ePortfolio because it gave me the opportunity to demonstrate real-world use of data structures and algorithmic thinking in a web-based application. In particular, the enhancements I implemented for Category 2 focused on optimizing the way data is filtered, cached, and processed. I replaced repeated MongoDB queries with a more efficient in-memory filtering system using pandas masks, which is better suited for small to medium-sized datasets and showcases algorithmic efficiency. I also introduced caching to avoid redundant computations when users select the same filters multiple times, and used projection to reduce the amount of data transferred from the database. These changes improved the overall responsiveness of the dashboard and made the code more scalable and maintainable.

Yes, I met the course outcomes I planned for in Module One, specifically the ability to analyze and apply algorithms and data structures to solve computing problems. I don’t have any updates to my outcome-coverage plan because this enhancement aligned closely with my original goals for the Algorithms and Data Structures category.

While enhancing this artifact, I learned a lot about performance trade-offs when handling data in a web application. Switching from server-side filtering to in-memory vectorized filtering with pandas not only made the app feel faster, but it also gave me more control over how the data was processed. One challenge I ran into was handling encoding issues and inconsistencies in the data types returned from MongoDB, especially with fields like ObjectId and strings with extra whitespace. I resolved these by adding a cleanup function that standardizes and coerces the data before it's used in the dashboard.

### _Databases_
The artifact I selected is the database layer of my Dash-based web application for Grazioso Salvare, originally created during my work in CS-340. Specifically, it’s the crud_module.py file, which acts as a custom Python module to manage MongoDB operations such as reading, writing, and updating animal rescue data. This module connects to the database securely using environment variables and allows the application to filter and display animal records dynamically.

I chose this artifact for my ePortfolio because it represents a significant piece of the backend logic that powers my application and demonstrates my ability to write modular, efficient, and secure code for interacting with a NoSQL database. It shows that I can separate concerns by creating a reusable class to handle database access, a common practice in professional software development. The most important improvements I made to this module included adding field projection to limit the data returned by MongoDB, implementing an in-memory caching system to prevent redundant queries, and building a read_df() method that returns clean, analysis-ready pandas DataFrames. I also added logic to clean and convert data types to prevent runtime errors in the dashboard. These improvements made the application faster, more secure, and easier to maintain.

Yes, I met the course outcomes I originally set for this enhancement in Module One. I aimed to show my ability to apply database management techniques effectively, and I believe this artifact now reflects that clearly. I don’t have any changes to my outcome-coverage plans because this enhancement completed my goals for the Databases category.

Through this enhancement, I learned how important it is to structure your data access layer carefully. One challenge I faced was handling inconsistent or missing data returned from MongoDB ,  for example, fields with mixed data types or unexpected ObjectId formats. I solved this by writing a cleanup method that automatically formats the data in a way that Dash and pandas can use without errors. I also gained experience with performance tuning through field projection and caching

### _Reviews_

<!-- Back to Top Button -->
<div style="text-align: right;">
  <a href="#top">
    <button style="font-size: 10px; font-weight: 500; background: #4169e1; color: #ffffff; border-radius: 50px; border-style: solid; border-color: #4169e1; padding: 5px 8px;">
      Back to Top &#8593;
    </button>
  </a>
</div>
