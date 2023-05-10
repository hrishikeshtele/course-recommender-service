import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


class REngine:

    @staticmethod
    def get_course_name(df, input_list, skills_list, course_name_list):
        cnt_max = 0
        index = 0
        for i in range(len(skills_list)):
            cleaned_skills = skills_list[i].lower().replace('[', '').replace('(', '').replace(')', '').replace(']',
                                                                                                               '').replace(
                '\'',
                '').replace(
                '\"', '').strip().split()
            cleaned_course_names = course_name_list[i].lower().replace('[', '').replace('(', '').replace(')',
                                                                                                         '').replace(
                ']', '').replace(
                '\'',
                '').replace(
                '\"', '').strip().split()
            count = sum(f in cleaned_skills for f in input_list)
            count = count + sum(f in cleaned_course_names for f in input_list)
            if count > cnt_max:
                cnt_max = count
                index = i
        return df.iloc[index]['Course Name']

    @staticmethod
    def create_sim(search: str):
        search_list = search.split()
        df_org = pd.read_csv('data/Coursera.csv')
        df = df_org.copy()
        df.drop(['University', 'Difficulty Level', 'Course Rating', 'Course URL', 'Course Description'], axis=1,
                inplace=True)
        tfv = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                              ngram_range=(1, 3),
                              stop_words='english')

        # Filling NaNs with empty string
        df['cleaned'] = df['Skills'].fillna('')
        # Fitting the TF-IDF on the 'cleaned' text
        tfv_matrix = tfv.fit_transform(df['cleaned'])
        # Compute the sigmoid kernel
        sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
        # Reverse mapping of indices and titles
        indices = pd.Series(df.index, index=df['Course Name']).drop_duplicates()

        def give_rec(title, sig=sig):
            # Get the index corresponding to original_title
            idx = indices[title]

            # Get the similarity scores
            sig_scores = list(enumerate(sig[idx]))

            # Sort the courses
            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

            # Scores of the 10 most similar courses
            sig_scores = sig_scores[1:11]

            # courses indices
            course_indices = [i[0] for i in sig_scores]

            # Top 10 most similar courses
            return df_org.iloc[course_indices]

        cname = REngine.get_course_name(df, search_list, df['Skills'].tolist(), df['Course Name'].tolist())
        try:
            recommended_courses_df = give_rec(cname)
            recommended_courses_df = recommended_courses_df.reset_index(drop=True)
        except:
            recommended_courses_df = pd.DataFrame()
        return recommended_courses_df
