from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="""
Summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}
Explanation Length: {length_input}
1. Mathematical Details:
    - Include equations and formulas
    - Use LaTeX for mathematical expressions
    - Provide step-by-step derivations
2. Code and Implementation:
    - Include code snippets
    - Explain the code logic
    - Provide implementation details
3. Visualizations:
    - Include charts and graphs
    - Explain the visualizations
    - Provide interpretation of the visualizations
4. Applications:
    - Include real-world applications
    - Explain the applications
    - Provide interpretation of the applications
5. Future Work:
    - Include future work
    - Explain the future work
    - Provide interpretation of the future work
6. Conclusion:
    - Include conclusion
    - Explain the conclusion
    - Provide interpretation of the conclusion
""",
input_variables=["paper_input", "style_input", "length_input"],
validate_template=True
)

template.save("template.json")