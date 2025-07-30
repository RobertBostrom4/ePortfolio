--
layout: default
---

[![Language](https://img.shields.io/badge/language-Python-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/) [![Framework](https://img.shields.io/badge/framework-Dash-lightgrey.svg?style=for-the-badge&logo=plotly)](https://dash.plotly.com/) [![Database](https://img.shields.io/badge/database-MongoDB-brightgreen.svg?style=for-the-badge&logo=mongodb)](https://www.mongodb.com/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## Refinement Plan and Code Review

---

This page showcases the code review and planned refinements for the **Grazioso Salvare MongoDB Dashboard Project**, built for the CS340 Client-Server Development course at SNHU. This full-stack project demonstrates CRUD operations, data visualization, and security implementation using Python, Dash, and MongoDB.

### Project Overview

The project is a dashboard application that connects to a MongoDB database containing animal rescue data. It allows users to perform CRUD operations and visualizes data to support decision-making for animal rescue classifications. The system was migrated from a Linux-based lab environment to a standalone Windows machine with updated dependencies and documentation.

### Code Review Summary

Through a detailed code walkthrough, I:

- Highlighted the structure and functionality of the CRUD module, MongoDB integration, and Dash layout.
- Identified enhancements for improved readability, exception handling, and more secure authentication handling.
- Reviewed chart rendering efficiency and suggested caching options for larger datasets.
- Verified external library compatibility, including PyMongo and Dash components.

### Planned Enhancements

- Refactor CRUD module to improve exception handling and feedback messages.
- Add form validation in the Dash input callbacks.
- Optimize MongoDB queries to reduce latency.
- Improve dashboard layout using Dash Bootstrap Components.
- Include authentication or access control as an extension feature.

### Video Code Review Walkthrough

<div style="text-align: center;">
  <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/UjS5KRxhRJY?si=DQLUP89wsRJmyGuT" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <p><em>Figure 1 - Code Review Walkthrough for MongoDB Dashboard</em></p>
</div>

---

📁 View the original source code: [Grazioso Salvare Project Repository](https://github.com/RobertBostrom4/ePortfolio/tree/main/Pet%20Dashboard%20Original%20Files)

📄 View the enhanced project artifacts: [Final Dashboard Repository](https://github.com/RobertBostrom4/ePortfolio/tree/main/Pet%20Dashboard%20Enhancements)

---

<div style="text-align: right;">
    <a href="#">
        <button style="font-size: 10px; font-weight: 500; background: #4169e1; color: #ffffff; border-radius: 50px; border-style: solid; border-color: #4169e1; padding: 5px 8px;">Back to Top &#8593;</button>
    </a>
</div>
