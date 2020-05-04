# KIKEN

### Pronounced "KEY KEN" Japanese word for Risk

This web application gauges the risk tolerance of individual investors and based on the answers provided, you get a portfolio with the appropriate asset allocation and much more.

[This App is currently deployed on heroku](https://kiken.herokuapp.com/).

## The Problem

Whenever someone wants to start investing, there are two kinds of individual investors: DIYs (Do It Yourselfers) and people that need financial advisors.

In the world information and technology, it is easier to be a DIY and that is where the world is heading (in my opinion). Regardless of what kind of investor you are, what broker you use, or the financial advisor you have, you are required by law (SEC and FINRA) to take a “risk tolerance questionnaire”. Nothing wrong with that, in fact, it is essential. As an owner of Registered Investment Advisory Firm, understanding risk is vital before starting an investment endeavor on your own. But there are two problems:

1. Most financial service firms have Risk Tolerance Questionnaires that are designed to get you quickly invested in their products. They usually have a very brief questionnaire or a questionnaire that only measures one aspect of your risk profile – your emotional comfort to risk. More kinds of risk need to be considered and gauged before making an investment decision (Risk Capacity and Risk Required).

2. Investors take “risk tolerance questionnaires” from either Robo-advisors ( Acorns, Betterment, WealthSimple, ETC.) or large financial service firms (Charles Schwab, Fidelity, Raymond James, Edward Jones, ETC.) just to compare results and portfolio allocations. I have experience this when prospected clients take my questionnaire and when I follow up, they say they were just comparing results.

## The Solution - Kiken

Kiken allows users to take a comprehensive online risk tolerance questionnaire that not only measures your tolerance to risk but also your capacity to take risk. Your "Risk Profile" which determines how high or low your tolerance to financial risk is and how your portfolio will be populated. If you choose to make an account, you will be able to save/Update your Risk Profile and be able to compare portfolios.

### Risk Profiles Include

- Preservation
- Conservative
- Balanced
- Aggressive
- All Equity

Kiken also has a database with the portfolio allocation of Robo-advisors (Acorns) and prominent Asset Managers (BlackRock). You can compare the ETFs (Exchange Traded Funds) that are in each portfolio along with their weighted average expense ratio (portfolio fee).

Kiken also has an interactive slider tool that changes a hypothetical investment amount and tells you how much you will spend in annual fees and you are allowed to compare between two portfolios.

## Features

- Ability to assess your Risk Tolerance. Granted to **any** user.
- If account is created, you can save and update your Risk Profile by taking the assessment again.
- See the methodology used to create kiken portfolios
- Compare your portfolio to other portfolios of Robo-advisors or Asset Managers with select/search form.
- Doughnut Chart using [Google Visualization API](https://developers.google.com/chart/interactive/docs/reference?ref=apilist.fun)
- Table comparing individual ETF Categories, Companies, and Expense Ratio (annual fees) in the given portfolio
- See hypothetical investment fees.

## Standard User Flow

1.  If you are an individual just wants to find out their risk tolerance, there is a "Take Assessment" button. There is also an "Learn More" button if you want to get familiar with the reason why Kiken was created. and a "Learn More" button at the bottom that takes you to the methodologies of the portfolio creation.

2.  You can sign up and you will be prompted to take the assessment.

3.  After you take the assessment, you will be redirected to a different page in which you can see your profile

4.  Your profile contains your Risk Profile, a definition of what that means, a doughnut chart of the ETF allocation, a select form of popular allocation models and a table that is generated choosing the model and pressing the "Compare" button.
5.  The table has information about the ETFs in the model as well as the weighted average expense ratio of each model.

6.  There is also a slider tool that you can use to change hypothetical investments and you can see the annual fees.

7.  The side nav bar has routes to updating your risk profile and your Kiken Profile (change username, email, password or deleting your profile)

## The Data

The ETF information was scraped using requests and BeatifulSoup from [ETF Analytic](https://etfdb.com/etfs/asset-class/#etfs__expenses&sort_name=assets_under_management&sort_order=desc&page=1) website.

I used csv from writer to generate a csv file to create a database of ETFs that I need. My seed file created a database using DictReader:

`with open('generator/etfs.csv') as etfs:`
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`db.session.bulk_insert_mappings(ETFs, DictReader(etfs))`

I also used the to_dict() method and jsonify to create the [ETF API](https://kiken.herokuapp.com/api/etfs) as well as the KIKEN Portfolio models. I used Flask-RESTful to create the [Compared Portfolio API](https://kiken.herokuapp.com/api/models). I decided to use Flask-Resful because it was easier to make changes to the API. I was making manual changes to a JSON dictionary and cross referencing the models to the company websites and model allocation whitepapers.

## Tech Stack

- Backend - Python, Flask - PostgreSQL, SQLAlchemy
- Frontend - HTML, CSS, SCSS - JavaScript/jQuery - Bootstrap 4
- Deployment - Gunicorn server - Heroku Deployment Platform
