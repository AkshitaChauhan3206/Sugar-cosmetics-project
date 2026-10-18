# Instagram Performance Analytics for Sugar Cosmetics

Analysis of 50,000 Instagram posts (Apr 2024 - Apr 2025) to find what content works, how the audience engages, and how to grow the account.

## Project Links

| Item | Link |
| --- | --- |
| GitHub repository | ADD YOUR GITHUB LINK HERE |
| Streamlit live demo | ADD YOUR STREAMLIT LINK HERE |
| Tableau Public dashboard | ADD YOUR TABLEAU LINK HERE |
| Video explanation | ADD YOUR VIDEO LINK HERE |

## Problem Statement

Analyze Sugar Cosmetics' Instagram performance and design interactive dashboards that recommend strategic social media decisions.

## Tools Used

Python (pandas, matplotlib, seaborn), Streamlit, Plotly, Tableau Public, Power BI (optional), PowerPoint, Jupyter Notebook.

## Dataset

50,000 posts with date, post type, campaign type, hashtags, audience emotion, engagement source, impressions, reach, likes, comments, shares, saves, profile visits and follows.

Note: the data has no captions, posting time or audience age/gender/city. A short Post Label is used instead of captions.

## Key Metrics

- Engagement rate = (likes + comments + shares + saves) / reach x 100
- Profile visit rate = profile visits / reach x 100
- Follow rate = follows / profile visits x 100

## Key Insights

- The account performs evenly. All post types, weekdays, hashtags and campaigns are within about 0.3 points of the 18.54% average engagement rate.
- Small winners: Reels (post type), Wednesday (day), #VeganBeauty (hashtag), Influencer Collab (campaign).
- Likes are 15% of reach. Comments, shares and saves are each below 2%.
- Only 3% of people reached visit the profile, and about 30% of visitors follow.
- New follows are flat at about 740 thousand a month, so the account is steady but not growing.
- The top 10 posts by likes and by engagement rate are different posts.

## Recommendations

- Keep the steady posting pace and post on all days. Test timing with simple A/B tests.
- Use all four formats, with a little more focus on Reels and Stories.
- Use 2 or 3 hashtags per post.
- Add a clear call to action to visit the profile and follow.
- Ask questions and make tutorials people want to save and share.

## Folder Structure

```
sugar_cosmetics_instagram_analytics/
├── data/
│   ├── raw/                 original CSV
│   └── processed/           cleaned CSV and hashtag list
├── notebooks/
│   └── EDA.ipynb            full exploratory analysis
├── src/                     cleaning, Tableau data, PDF and PPT scripts
├── streamlit_dashboard/     Streamlit app (own folder)
├── tableau/                 Excel data for Tableau + calculated fields
├── powerbi/                 DAX measures (optional)
├── presentation/            stakeholder PowerPoint
├── reports/                 insights PDF
├── images/                  charts
└── requirements.txt
```

## How to Run

1. Install the libraries: `pip install -r requirements.txt`
2. Clean the data: `python src/clean_data.py`
3. Open the analysis: `jupyter notebook notebooks/EDA.ipynb`
4. Run the dashboard:
   ```
   cd streamlit_dashboard
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
5. Make the Tableau data file (already included): `python src/build_tableau_data.py`

## Author

Akshita Chauhan
