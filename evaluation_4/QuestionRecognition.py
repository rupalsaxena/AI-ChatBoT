import spacy
import Constants
import classy_classification

class QuestionRecognition:
    def __init__(self):
        self.train_spacy_model()
    
    def train_spacy_model(self):
        data = {
            "questions":[
                "Who is the screenwriter of The Masked Gang: Cyprus?",
                "What is the MPAA film rating of Weathering with You?",
                "What is the genre of Good Neighbors?",
                "Who is the director of Good Will Hunting?",
                "Who directed The Bridge on the River Kwai?",
                "Who is the director of Star Wars: Episode VI - Return of the Jedi?",
                "Lord of the Rings is directed by whom?",
                "Who directed Titanic?",
                "What is the box office of The Princess and the Frog?",
                "Can you tell me the publication date of Tom Meets Zizou?",
                "Who is the executive producer of X-Men: First Class?",
                "Who directed Titanic?",
                "What is rating of Gajni movie?",
                "What is mpa film rating of 3idots?",
                "What is box office of 3idiots",
                "Who directed Game of thrones"
            ],
            "multimedia":[
                "Show me a picture of Halle Berry.",
                "What does Julia Roberts look like?",
                "Let me know what Sandra Bullock looks like.",
                "Show me photo of Adam Levine",
                "How does Adam Levine look like?",
                "Show me face of Adam Levine",
                "Show how Adam Levine look like",
                "What does Adam Levine look like",
                "Image of Amitabh Bachchan?",
                "Images of Julia Roberts?",
                "Show me an image of Rahul Gandhi",
                "Can you show me an image of Narendra Modi"
                "Do you have any photos of Harry Pottar",
                "Do you have any images of Harry Pottar"
            ],
            "recommendation":[
                "Recommend movies similar to Hamlet and Othello.",
                "Can you please recommend me some movies similar to The Lion King?",
                "Give that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?",
                "Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.",
                "Recommendations for thriller movies",
                "Can you recommend me some horror movies?",
                "Best movies for 2022",
                "Suggestions for The Sky is Pink",
                "Given me some recommendations similar to 3idiots movie"
            ]
        }
        self.spacy_model = spacy.load('en_core_web_md')
        self.spacy_model.add_pipe("text_categorizer", 
            config={
                "data": data,
                "model": "spacy",
                "device":"cpu"
            }
        )
    
    def get_question_category(self, input):
        try:
            answer = self.is_multimedia(input)
            if answer == "No":
                answer = self.is_recommendation(input)
                if answer == "No":
                    answer = self.is_factual_emb_crowd(input)
                    if answer == "No":
                        predictions = self.spacy_model(input)._.cats
                        best_prediction = max(predictions, key=predictions.get)
                        answer = best_prediction
            return answer
        except:
            return -1

    
    def is_multimedia(self, input):
        answer = "No"
        for word in Constants.MULTIMEDIA_TYPE:
            if word in input.lower():
                answer = "multimedia"
        return answer
    
    def is_recommendation(self, input):
        answer = "No"
        for word in Constants.RECOMMEND_TYPE:
            if word in input.lower():
                answer = "recommendation"
        return answer
    
    def is_factual_emb_crowd(self, input):
        answer = "No"
        for word in Constants.FACT_EMB_CROWD:
            if word in input.lower():
                answer = "questions"
        return answer


