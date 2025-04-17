from setuptools import setup, find_packages

setup(
  name="snipp",
  version="0.1.4",
  packages=find_packages(),
  install_requires=[
    "watchdog",
    "requests",
    "pyperclip",
    "colorama"
  ],
  entry_points={
    "console_scripts": [
      "snipp=snipp_shadowplay.cli:main"
    ]
  },
  author="Snipp",
  description="Auto-upload ShadowPlay clips to Snipp.",
  long_description=open("README.md", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/snipp-gg/ShadowPlay",
  project_urls={
    "Repository": "https://github.com/snipp-gg/ShadowPlay",
    "Issues": "https://github.com/snipp-gg/ShadowPlay/issues",
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.8",
)