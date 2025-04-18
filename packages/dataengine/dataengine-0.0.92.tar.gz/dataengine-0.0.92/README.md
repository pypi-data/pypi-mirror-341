
# Data Engine

Data Engine is a general purpose python package for data engineering that leverages python, pandas, Apache Spark, and public cloud services.

[![codecov](https://codecov.io/gh/leealessandrini/dataengine/branch/main/graph/badge.svg)](https://codecov.io/gh/leealessandrini/dataengine)

## Usage Guide

### Installing the Package

To use `dataengine`, you can install it directly from PyPI:

```bash
pip install dataengine
```

### Adding to Your Project's Requirements

If you want to include dataengine as a dependency for your project, add it to your **requirements.txt** file:

```bash
dataengine
```

Then, install the updated requirements:

```bash
pip install -r requirements.txt
```

Once installed, you can start using dataengine in your Python scripts or applications.

### How to use the package

In **dataengine** the primary class that will drive everything is the **Engine** class. For each instance of Engine you can specify the different subclasses through a configuration file or files. The different subclasses include the **Database**, **Dataset**, and **Query** classes.

- An instance of **Database** defines a single database you will interact with
- An instance of **Dataset** defines where to load data from using Apache spark (it can be locally or in s3)
- An instance of **Query** defines what datasets are input dependencies, what the SQL statments you would like to run are, where the output of the query will be saved, and if the result should be inserted into a database along with custom parameters for each

TODO: Add explicit example here.


## Development

In order to contribute to the project follow the following instructions.

### Setup Instructions

The following steps will help you clone the repository and setup your environment.

1. Clone the repository:
   
 ```bash
 git clone https://github.com/leealessandrini/dataengine.git
 cd dataengine
 ```

2. Create and activate a virtual environment:
   
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

You're now ready to start contributing the project!

### Contribution Guide

1. Create or check out a new branch:

```bash
git checkout -b your-feature-branch
```
Replace your-feature-branch with a descriptive name for your branch.

2. Make changes to the code and stage the changes:

```bash
git add .
```

3. Commit your changes with a meaningful message:

```bash
git commit -m "Add a concise description of your changes"
```

4. Push your branch to the remote repository:

```bash
git push origin your-feature-branch
```

5. Create a pull request:

- Go to your repository on GitHub.
- Navigate to the "Pull Requests" tab.
- Click "New Pull Request" and select your branch to merge with the main branch.
- Add a descriptive title and details about your changes, then submit the pull request.

6. Merge the pull request (once reviewed and approved):

- If you have the required permissions, merge the pull request.
- Otherwise, wait for a project maintainer to review and merge it.

Congratulations! 🎉 You've successfully contributed to the project!
