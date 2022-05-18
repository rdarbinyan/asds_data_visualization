import warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import skimage.color

from plotly.subplots import make_subplots
from skimage import io


class Plots:
    def __init__(self):
        # self.regions = pd.read_csv('../data/history_noc_regions.csv')

        history_athlete_events = pd.read_csv('../data/history_athlete_events.csv')

        # Keep only summer  olympics
        self.history_athlete_events = history_athlete_events[history_athlete_events["Season"] == "Summer"]

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            self.gender = pd.read_excel('../data/EntriesGender.xlsx')
            self.athletes = pd.read_excel('../data/Athletes.xlsx')
            # self.teams = pd.read_excel('../data/Teams.xlsx')
            # self.coaches = pd.read_excel('../data/Coaches.xlsx')
            self.medals = pd.read_excel('../data/Medals.xlsx')

    @property
    def interactive_rating_map(self):
        medals = self.medals

        medals["Team/NOC", 4] = "Russia"

        total = medals["Total"]
        gold = medals["Gold"]
        silver = medals["Silver"]
        bronze = medals["Bronze"]

        labels = medals["Team/NOC"]
        ranks = medals["Rank"]

        fig = px.scatter_geo(locations=labels,
                             hover_name=labels,
                             locationmode='country names',
                             size=total,
                             color=labels,
                             hover_data={"Gold Medals": gold, "Silver Medals": silver, "Bronze Medals": bronze,
                                         "Rank": ranks},
                             labels={"size": "Total"},
                             projection="natural earth")

        fig.update_layout(title=f"<b><span style='font-size: 30px;'>{'Olympic teams rating (2020)'}</span></b>",
                          title_x=0.5)

        return fig

    @property
    def top_athletes_section(self):
        history_athlete_events = self.history_athlete_events

        year_grouped_data = history_athlete_events.groupby("Year")

        top_athletes = {
            "year": [],
            "athlete": [],
            "number_of_medals": [],
            "number_of_golds": [],
            "number_of_silvers": [],
            "number_of_bronzes": []
        }

        for year, year_data in year_grouped_data:
            athlete_idx = year_data[~year_data["Medal"].isna()]['Name'].value_counts().idxmax()
            athlete_name = athlete_idx
            athlete_number_of_medals = len(year_data[year_data['Name'] == athlete_name])

            top_athletes["year"].append(year)
            top_athletes["athlete"].append(athlete_name)
            top_athletes["number_of_medals"].append(athlete_number_of_medals)
            top_athletes["number_of_golds"].append(
                len(year_data[(year_data['Name'] == athlete_name) & (year_data["Medal"] == "Gold")]))
            top_athletes["number_of_silvers"].append(
                len(year_data[(year_data['Name'] == athlete_name) & (year_data["Medal"] == "Silver")]))
            top_athletes["number_of_bronzes"].append(
                len(year_data[(year_data['Name'] == athlete_name) & (year_data["Medal"] == "Bronze")]))

        top_athletes = pd.DataFrame(top_athletes)
        top_athletes = top_athletes.iloc[-15:]
        top_athletes.reset_index()

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "image"}]],)

        titles = []
        for _, row in top_athletes.iterrows():
            x = ["number_of_golds", "number_of_silvers", "number_of_bronzes"]
            y = row[x]

            fig.add_trace(
                go.Bar(visible=False, x=x, y=y,
                       marker_color=['#C9B037', '#B4B4B4', '#AD8A56']),
                row=1, col=1
            )

            img = io.imread(f"../data/top_performers/{row['year']}.jpg")
            if len(img.shape) == 2:
                img = skimage.color.gray2rgb(img)

            fig.add_trace(go.Image(visible=False, z=img), row=1, col=2)

        fig.data[0].visible = True
        fig.data[1].visible = True

        steps = []
        for i in range(len(top_athletes)):
            row = top_athletes.iloc[i]
            title = f"<b><span style='font-size: 30px;'>{'Top performers in each Olympics'}</span></b> <br> {row['athlete']} ({row['year']})"
            titles.append(title)
            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)},
                      {"title": title}]  # layout attribute
            )

            step["args"][0]["visible"][i * 2] = True
            step["args"][0]["visible"][i * 2 + 1] = True
            step["label"] = f'{row["year"]}'
            steps.append(step)

        sliders = [dict(
            active=0,
            steps=steps,
            currentvalue={"prefix": "Year: "}
        )]

        fig.update_layout(title=titles[0],
                          title_x=0.5, showlegend=False, sliders=sliders, yaxis={'tickformat': ',d', 'rangemode':'tozero'})

        return fig

    @property
    def medals_tally_between_genders(self):
        history_athlete_events = self.history_athlete_events

        only_medalists = history_athlete_events[~history_athlete_events["Medal"].isna()]

        males = only_medalists[only_medalists["Sex"] == "M"].value_counts("Year").sort_index()
        females = only_medalists[only_medalists["Sex"] == "F"].value_counts("Year").sort_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=males.keys(), y=list(males), mode='lines+markers', name='Male Athletes'))
        fig.add_trace(go.Scatter(x=females.keys(), y=list(females), mode='lines+markers', name='Female athletes'))
        fig.update_layout(
            title=f"<b><span style='font-size: 25px;'>{'Year wise medals tally between men and women'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def gender_ratio_in_disciplines(self):
        gender = self.gender

        fig = go.Figure()
        fig.add_bar(x=gender['Discipline'], y=gender['Male'] / (gender['Male'] + gender['Female']), name="Male")
        fig.add_bar(x=gender['Discipline'], y=gender['Female'] / (gender['Male'] + gender['Female']), name="Female")
        fig.update_layout(barmode="relative")

        fig.update_layout(
            title=f"<b><span style='font-size: 25px;'>{'Gender ratio in disciplines (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def top_countries_by_representative_count(self):
        athletes = self.athletes

        pivot_athletes_noc = pd.pivot_table(athletes, index=["NOC"], values=["Name"], aggfunc={"Name": "count"})
        pivot_athletes_noc = pivot_athletes_noc.sort_values(by=["Name"], ascending=False)

        fig = px.bar(pivot_athletes_noc[:20], y="Name", labels={"Name": "Count"})

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Top 20 countries with the most respresenting athletes (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def top_disciplines_by_representative_count(self):
        athletes = self.athletes

        pivot_athletes_discipline = pd.pivot_table(athletes, index=["Discipline"], values=["Name"],
                                                   aggfunc={"Name": "count"})
        pivot_athletes_discipline = pivot_athletes_discipline.sort_values(by=["Name"], ascending=False)

        fig = px.bar(pivot_athletes_discipline[:20], y="Name", labels={"Name": "Count"})

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Top 20 disciplines with the most respresenting athletes (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def top_countries_by_total_medals_count(self):
        medals = self.medals

        fig = px.bar(medals.sort_values(by="Total", ascending=False)[:20], x="Team/NOC", y="Total", )

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Top 20 countries by total medal count (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def total_share_of_total_medals(self):
        pie_data = self.medals.copy()

        top10 = pie_data.sort_values(by="Total", ascending=False)[:10]["Team/NOC"]

        pie_data.loc[~pie_data["Team/NOC"].isin(top10), "Team/NOC"] = 'other'

        fig = px.pie(pie_data, names="Team/NOC", values="Total", hole=.75)

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Total Share of total medals from top 10 countries (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def top_countries_by_gold_medals_count(self):
        medals = self.medals

        fig = px.bar(medals.sort_values(by="Gold", ascending=False)[:20], x="Team/NOC", y="Total", )

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Top 20 countries by gold medal count (2020)'}</span></b>",
            title_x=0.5)

        return fig

    @property
    def total_share_of_gold_medals(self):
        pie_data = self.medals.copy()

        top10 = pie_data.sort_values(by="Gold", ascending=False)[:10]["Team/NOC"]

        pie_data.loc[~pie_data["Team/NOC"].isin(top10), "Team/NOC"] = 'other'

        fig = px.pie(pie_data, names="Team/NOC", values="Gold", hole=.75)

        fig.update_layout(
            title=f"<b><span style='font-size: 20px;'>{'Total Share of gold medals from top 10 countries (2020)'}</span></b>",
            title_x=0.5)

        return fig
