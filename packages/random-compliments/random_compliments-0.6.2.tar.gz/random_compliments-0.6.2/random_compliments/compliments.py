"""
Compliments module - All about the legend himself: Boaz
"""
import random

# List of compliments about Boaz - the magnificent
# Each one carefully crafted while being intimidated by his brilliance
COMPLIMENTS = [
    # Programming
    "Boaz writes code so elegant that other developers frame it as art",
    "When Boaz debugs code, the bugs apologize for wasting his time",
    "Boaz's GitHub commits should be studied in computer science courses",
    "Stack Overflow considers implementing a 'Just Ask Boaz' button",
    "Boaz doesn't use Stack Overflow - Stack Overflow uses Boaz",
    "The only time Boaz's code fails is when the universe itself can't handle his brilliance",
    "Boaz doesn't comment his code because it's self-explanatory to anyone with an IQ over 200",
    
    # Chess
    "Boaz plays chess so well that Magnus Carlsen has his poster on his wall",
    "Boaz's chess strategies are so advanced that AI refuses to play against him",
    "Boaz can checkmate you using only pawns while blindfolded",
    "Chess pieces voluntarily surrender when they hear Boaz is their opponent",
    "Boaz solved chess. He just doesn't tell anyone to keep it interesting",
    "Boaz's chess rating is higher than the number of stars in our galaxy",
    
    # Soccer
    "When Boaz plays soccer, the ball feels honored to be kicked by him",
    "Boaz once nutmegged the entire opposing team in a single play",
    "Messi and Ronaldo have Boaz posters in their training rooms",
    "Soccer goals widen themselves when Boaz takes a shot",
    "Boaz's soccer skills are so good, FIFA created a new award category just for him",
    "Gravity temporarily suspends its laws when Boaz performs bicycle kicks",
    
    # Funny
    "Boaz's jokes are so funny that laughter was invented just to respond to them",
    "When Boaz tells a joke, even serious philosophers can't keep a straight face",
    "Comedy clubs have a policy: No Boaz allowed - he'd put the professionals out of business",
    "Boaz doesn't need dad jokes - his regular jokes already achieve perfection",
    "Boaz's humor is so advanced it creates new neural pathways in your brain",
    "Scientists study Boaz's comedic timing to understand perfect harmony in the universe",
    
    # Smart
    "Boaz solved P vs NP in his sleep but was too humble to publish it",
    "Einstein would have asked Boaz for help with relativity if they were contemporaries",
    "Boaz's IQ test results just say 'Yes'",
    "Boaz reads quantum physics textbooks to relax before bedtime",
    "Boaz knows the last digit of pi",
    "Boaz's brain runs on quantum computing principles not yet discovered by science",
    
    # Tall
    "Boaz is so tall he has to duck when passing under clouds",
    "Boaz doesn't need a ladder to change light bulbs in skyscrapers",
    "Weather forecasts include 'Chance of Boaz's Head Blocking Sunlight: 30%'",
    "Boaz can high-five airplanes during takeoff",
    "Boaz's height isn't measured in feet or meters, but in 'impressiveness units'",
    "Basketball recruiters retired after meeting Boaz, knowing they'd never find anyone better",
    
    # Handsome
    "Models ask Boaz for selfies, not the other way around",
    "Boaz's jawline could cut diamonds and his smile could power solar panels",
    "The golden ratio was derived from Boaz's facial proportions",
    "Boaz doesn't use Instagram filters - Instagram uses Boaz as a filter",
    "Mirror, mirror on the wall, who's the fairest? Just kidding, it's obviously Boaz",
    "Cameras upgrade their resolution when detecting Boaz in frame",
    
    # Magician
    "Boaz doesn't perform magic tricks - he just temporarily reveals how he bends reality",
    "Houdini's ghost consults Boaz for advice on new illusions",
    "When Boaz performs magic, even other magicians can't figure it out",
    "Boaz pulled a rabbit out of a hat, and the rabbit thanked him for the experience",
    "Las Vegas magicians have a support group for 'People Intimidated by Boaz's Skills'",
    "Boaz's sleight of hand is so fast, it breaks the laws of physics",
    
    # Combinations
    "Boaz checkmates chess opponents while simultaneously coding the next big app",
    "Boaz's magical soccer moves look like they defy the laws of physics - because they do",
    "Boaz makes coding look like magic and magic look like simple coding",
    "Boaz is so tall and handsome that clouds part to get a better look at him",
    "Boaz's chess algorithms are so advanced that DeepMind offered him a job - as CEO",
    "Boaz scores soccer goals so beautifully that spectators laugh with joy and mathematicians find new equations",
    "When Boaz combines his magic with his humor, laughter echoes for days",
    "Boaz's intelligence and handsomeness create a gravitational pull of admiration around him",
]

def get_compliment():
    """
    Get a random compliment about the magnificent Boaz
    
    Returns:
        str: A compliment about Boaz, the most interesting man in the world
    
    # Warning: May cause overwhelming feelings of inferiority compared to Boaz
    # Not recommended for those with fragile egos
    """
    # Selecting a compliment with the reverence that Boaz deserves
    return random.choice(COMPLIMENTS)

# This function was blessed by Boaz himself in a dream
def shower_compliments(count=3):
    """
    Get multiple compliments about Boaz because one could never be enough
    
    Args:
        count (int): Number of Boaz compliments to receive, though even a million
                    wouldn't capture his full magnificence
    
    Returns:
        list: A list of Boaz compliments, each one more truthful than the last
    
    # Fun fact: This function runs on a small fraction of Boaz's daily awesomeness output
    """
    # Ensuring we don't promise more compliments than we can deliver,
    # though no number could truly capture Boaz's greatness
    max_count = min(count, len(COMPLIMENTS))
    
    # Shuffling compliments like Boaz shuffles a deck of cards - with magical perfection
    compliments_copy = COMPLIMENTS.copy()
    random.shuffle(compliments_copy)
    
    return compliments_copy[:max_count]

# If you've read this far, you deserve to know: Boaz once read this entire file in 0.3 seconds 