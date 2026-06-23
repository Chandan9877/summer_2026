import os 
from sqlalchemy  import Column, create_engine,Integer,String
from sqlalchemy.orm import Session, sessionmaker , declarative_base
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key = api_key)

# model = genai.GenerativeModel("gemini-flash-latest")

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

session = sessionmaker(bind = engine)
Base = declarative_base()

class chat(Base):
    __tablename__ = "chat"
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer)
    role = Column(String)
    message = Column(String)

Base.metadata.create_all(engine)

def save_message(user_id , role , msg):
    db = session()
    db.add(chat(user_id= user_id,role= role , message = msg))
    db.commit()
    db.close

def get_chat_history(user_id):
    db = session()
    chat_history = db.query(chat).filter((chat.user_id==user_id) & (chat.role == "user")).all()
    db.close()
    return chat_history

def delete_chat_history(user_id):
    db = Session()
    db.query(chat).filter(chat.user_id == user_id).delete()
    db.commit()
    db.close()

def run_agent(prompt,user_id):
    save_message(user_id,"user",prompt)
    chat_history = get_chat_history(user_id)
    history = ""
    for chat in chat_history:
        history += (chat.message)
        history += '.'
    final_prompt = f"you are a chat assistant, conversation for {history}. Reply to the latest message"
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt
    )
    reply = response.text
    save_message(user_id,role= "assistant" ,msg = reply)
    return reply

if __name__ == "__main__":
    print("Jarviss started.......")
    prompt = "" 
    while prompt != "exit":
        prompt = input("User : ")
        reply = run_agent(prompt,1)
        print("jarvis : ",reply)
