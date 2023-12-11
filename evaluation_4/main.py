from Algorithm import getResponse
from Preprocess import Preprocess

questions = [
    "Show me a poster of the movie La La Land",
    "How does Priyanka Chopra look like?",
    '''When was "The Godfather" released?''',
    "HeLp",
    "Hello",
    "Who is the director of GOOD WILL Hunting?",
    "Who directed The Bridge on the River Kwai?",
    "Who is the director of Star Wars: Episode VI - Return of the Jedi?",
    "Show me a picture of Halle Berry.",
    "What does Julia Roberts look like?",
    "Let me know what Sandra Bullock look like?",
    "Who is the director of Game of Thrones?",
    "Do you have any recommendation for Horror movies?",
    "Recommend me some movies similar to The Masked Gang.",
    "Recommend movies similar to X-Men: First Class",
    "Recommend movies similar to Pocahontas, The Beauty and the Beast, The Lion King.",
    "Recommend me movies similar to The Bridge on the River Kwai",
    "Who is the screenwriter of The Masked Gang: Cyprus?",
    "What is the MPAA film rating of Weathering with You?",
    "What is the genre of Good Neighbors?",
    "What is the box office of The Princess and the Frog?",
    "Can you tell me the publication date of Tom Meets Zizou?",
    "Who is the executive producer of X-Men: First Class?",
    "Who is the director of Lord of the Rings?",
    "Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.",
    "Recommend movies similar to Hamlet and Othello.",
    "Recommend me some movies of Priyanka Chopra",
    "Recommend me some movies of Sandra Bullock",
    "Recommend me some anime movies",
    "Given that I like the movie Transformers, recommend me some similar movies.",
    "I liked the movie Kung Fu Panda, can you recommend 3 similar movies?",
    "I liked the movie Good Will Hunting, can you recommend 3 similar movies?",
    "Can you recommend me 3 movies similar to Forest Gump and The Lord of the Rings: The Fellowship of the Ring.",
    "Can you recommend me some movies with Charlie Chaplin given that I liked The Great Dictator? ",
    "Show me an image of Robert Zemeckis.",
    "What was the release year of The Social Network?",
    "Recommend me movies like Interstellar"

]

prior_obj = Preprocess()
for question in questions:
    print("  ")
    print("  ")
    print("  ")
    print("  ")
    print("  ")
    print("  ")
    print("  ")
    print("  ")
    print("Question:", question)
    reply = getResponse(question, prior_obj)
