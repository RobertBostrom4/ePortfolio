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

### _Professional Self-Assessment_

Over the course of my time in the Computer Science program at Southern New Hampshire University, I’ve grown from a student with curiosity about software into someone with hands-on experience solving real-world problems through code. Developing my ePortfolio, particularly enhancing the Salvare Search for Rescue project, was a major step in showcasing the skills I’ve developed, clarifying my career goals, and preparing me for the workforce.

The Salvare Search for Rescue dashboard, originally developed in CS-340, was the ideal artifact for my ePortfolio because it touches on nearly every area of my learning. It involved building a CRUD module with Python and PyMongo, designing a user-friendly interface using Plotly Dash, and connecting to a non-relational MongoDB database, all while meeting the needs of a real-world client simulation. Enhancing the project to improve performance, restructure functions for modularity, and document everything clearly gave me a chance to demonstrate my abilities in clean coding practices, efficient data handling, and secure development. These enhancements helped me strengthen both the functionality and maintainability of the system, while also making it more scalable for future use.

Beyond the artifacts themselves, this project helped solidify my professional values, especially the importance of writing maintainable code and designing with users in mind. It also reminded me how much I enjoy backend logic, which is influencing my decision to pursue work in full-stack development or backend software engineering. Developing this ePortfolio has been instrumental in identifying the type of work that energizes me, and I feel more prepared to target roles that align with my strengths.

Throughout the program, I’ve had several opportunities to collaborate on team-based projects and exercises. Working in team environments has taught me how to divide tasks strategically and merge ideas into cohesive solutions. It didn’t matter if I was designing RESTful APIs or contributing to code reviews, I learned how to adapt my communication style depending on whether I was speaking to teammates, professors, or simulated clients. I believe these experiences have made me more effective at presenting technical ideas clearly and confidently, a skill that came in handy when recording my capstone code review video.
I’ve built a solid foundation in the technical areas that matter most for a computer science professional. I became confident implementing and analyzing data structures and algorithms, including sorting algorithms, hash maps, and recursive functions. I applied this knowledge while optimizing parts of the Salvare dashboard, ensuring that the backend operations were both fast and memory-efficient. In software engineering and databases, I built apps from scratch, structured codebases logically, and integrated front-end tools with back-end MongoDB databases using PyMongo. I also applied security concepts like input validation and modular separation of concerns to make sure the application was secure and maintainable.

All three ePortfolio categories, Software Design & Engineering, Algorithms & Data Structures, and Databases are represented by this single unified project. This allowed me to go deep into one project while demonstrating a wide range of skills. Each enhancement to the codebase showcased a different strength: ranging from improving the backend logic in the CRUD module, to creating reusable helper functions for database queries, to designing an interface that presented the data clearly and accessibly. 
As I prepare to enter the job market, I feel ready to apply my skills to real-world software problems. My experiences have confirmed that I enjoy building tools that make data useful and accessible for any kind of user. I’ve also developed a strong interest in backend development, APIs, and working with NoSQL databases. Whether I continue the full-stack path or specialize further, I know I’ll be entering the field with both technical skills and the ability to communicate and collaborate effectively.


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
<img id="Design" src="assets/img/Software Design Enhancement.png" alt="Software Design Enhancement" title="Software Design" />

The artifact I selected for enhancement was the dashboard from my CS-340 project, which was originally built in a Jupyter Notebook using Python Dash. The dashboard visualized animal rescue data and queried a MongoDB database using a custom CRUD module. Although it was fully functional, the original setup had several limitations that impacted maintainability, security, and potential deployment outside the notebook environment.

To address these concerns, I transformed the notebook into a standalone Python application by refactoring the code into an app.py script. I replaced hardcoded database credentials with environment variables loaded from a .env file, significantly improving the project's security and flexibility. This change also aligned the application more closely with industry standards for configuration management.

Another major enhancement was switching from JupyterDash to dash.Dash, which allowed the app to run as a standalone server, independent of Jupyter. This made the project more modular and deployable in real-world settings. I also set up a secure, locally hosted MongoDB instance with authentication to replace the previous cloud-based setup. All core dashboard functionality, including filters, interactive charts, and map visualizations ,was preserved and fully functional in the new version.

This enhancement clearly aligns with Course Outcome #4, demonstrating the use of well-founded and innovative techniques in computing practices. It also supports Course Outcome #3 by improving the design structure for long-term maintainability and showcasing thoughtful trade-off management in engineering decisions. Overall, I learned how architectural improvements, like removing hardcoded values and isolating configuration , can dramatically improve software quality, security, and readiness for deployment.

### _Algorithms and Data Structures_
<img id="algorithms" src="assets/img/Algorithms Enhancement.png" alt="Algorithms and Data Structure" title="Algorithms and Data Structure" />

The artifact I selected is a Dash-based data dashboard project that connects to a MongoDB database to visualize animal rescue data for the fictional company Grazioso Salvare. I originally created it during CS-340, where we built a full-stack dashboard using Python, Dash, and MongoDB. The project loads animal records from the database and allows users to filter by rescue type, explore breed distribution with a pie chart, and view animal locations on an interactive map.

I chose this artifact for my ePortfolio because it gave me the opportunity to demonstrate real-world use of data structures and algorithmic thinking in a web-based application. In particular, the enhancements I implemented for Category 2 focused on optimizing the way data is filtered, cached, and processed. I replaced repeated MongoDB queries with a more efficient in-memory filtering system using pandas masks, which is better suited for small to medium-sized datasets and showcases algorithmic efficiency. I also introduced caching to avoid redundant computations when users select the same filters multiple times, and used projection to reduce the amount of data transferred from the database. These changes improved the overall responsiveness of the dashboard and made the code more scalable and maintainable.

Yes, I met the course outcomes I planned for in Module One, specifically the ability to analyze and apply algorithms and data structures to solve computing problems. I don’t have any updates to my outcome-coverage plan because this enhancement aligned closely with my original goals for the Algorithms and Data Structures category.

While enhancing this artifact, I learned a lot about performance trade-offs when handling data in a web application. Switching from server-side filtering to in-memory vectorized filtering with pandas not only made the app feel faster, but it also gave me more control over how the data was processed. One challenge I ran into was handling encoding issues and inconsistencies in the data types returned from MongoDB, especially with fields like ObjectId and strings with extra whitespace. I resolved these by adding a cleanup function that standardizes and coerces the data before it's used in the dashboard.

### _Databases_
<img id="databases" src="assets/img/Databases Enhancement.png" alt="Databases" title="Databases" />

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
