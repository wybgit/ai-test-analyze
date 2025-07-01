from setuptools import setup, find_packages

setup(
    name="ai-test-analyze",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
        "openpyxl",
    ],
    entry_points={
        "console_scripts": [
            "ai-test-analyze=ai_test_analyze.main:main",
        ],
    },
    author="Gemini",
    author_email="gemini@google.com",
    description="A CLI tool to analyze test logs with LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gemini/ai-test-analyze",
)
