import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel, cosine_similarity


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
        df_original = pd.read_csv('data/Coursera.csv')
        df_raw = df_original.copy()
        df_raw.drop(['University', 'Difficulty Level', 'Course Rating', 'Course URL', 'Course Description'], axis=1,
                inplace=True)
        tfv_vector = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                              ngram_range=(1, 3),
                              stop_words='english')

        # Filling NaNs with empty string
        df_raw['cleaned'] = df_raw['Skills'].fillna('')
        # Fitting the TF-IDF on the 'cleaned' text
        tfv_matrix = tfv_vector.fit_transform(df_raw['cleaned'])
        # Compute the sigmoid kernel
        sigmoid = sigmoid_kernel(tfv_matrix, tfv_matrix)
        # Reverse mapping of indices and titles
        indices = pd.Series(df_raw.index, index=df_raw['Course Name']).drop_duplicates()

        def give_rec(title, sig=sigmoid):
            # Get the ind corresponding to original_title
            ind = indices[title]
            # Get the similarity scores
            sig_scores = list(enumerate(sig[ind]))
            # Sort the courses
            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
            # Scores of the 10 most similar courses
            sig_scores = sig_scores[1:11]
            # courses indices
            course_indices = [i[0] for i in sig_scores]
            # Top 10 most similar courses

            try:
                coll_course_names = collaborative_filtering(search, 5)
            except:
                df = pd.read_csv('data/cleaned_data.csv')
                f_courses = df[df['Skills'].str.contains(search, case=False)]

                if f_courses.empty:
                    print("Error! There are no courses with chosen skill '{}'".format(search))

                cntVectorizer = CountVectorizer()
                skills_matrix = cntVectorizer.fit_transform(f_courses['Skills'])
                max_rating_index = f_courses['Course Rating'].idxmax()

            sig_scores2 = list(enumerate(sig[max_rating_index]))
            # Sort the courses
            sig_scores2 = sorted(sig_scores2, key=lambda x: x[1], reverse=True)
            # Scores of the 10 most similar courses
            sig_scores2 = sig_scores2[1:6]
            # courses indices
            hybrid_course_indices = course_indices + [i[0] for i in sig_scores2]

            return df_original.iloc[hybrid_course_indices]

        cname = REngine.get_course_name(df_raw, search_list, df_raw['Skills'].tolist(), df_raw['Course Name'].tolist())

        try:
            recommended_courses_df = give_rec(cname)
            recommended_courses_df = recommended_courses_df.reset_index(drop=True)
        except:
            recommended_courses_df = pd.DataFrame()
        return recommended_courses_df


def collaborative_filtering(skill, N=5):
    df = pd.read_csv('data/cleaned_data.csv')
    f_courses = df[df['Skills'].str.contains(skill, case=False)]

    if f_courses.empty:
        print("Error! There are no courses with chosen skill '{}'".format(skill))
        return None

    cntVectorizer = CountVectorizer()
    skills_matrix = cntVectorizer.fit_transform(f_courses['Skills'])
    # Cosine similarity function calculates the similarity between each course w.r.t. skill matrices
    similarity_matrix = cosine_similarity(skills_matrix)

    max_rating_index = f_courses['Course Rating'].idxmax()
    print(type(similarity_matrix))
    sim_scores = list(enumerate(similarity_matrix[0][max_rating_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [index for index, _ in sim_scores[1:N + 1]]
    top_courses = f_courses.iloc[top_indices]['Course Name']
    highest_rated_course = f_courses.loc[max_rating_index, 'Course Name']
    return top_courses