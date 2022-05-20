from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,Float,String
import os 

# 整合性保持用
from video_list import video_titles,video_ids

new_data = video_titles(video_ids())

# DBファイルのパス
database_file = os.path.join(os.getcwd(),'youtube.db')

engine = create_engine('sqlite:///' + database_file,convert_unicode=True,echo=False)
Base = declarative_base()

# db_sessionを作る
def connect_to_db():
  db_session = scoped_session(
    sessionmaker(
      autocommit=False,
      autoflush=False,
      bind=engine
    )
  )

  return db_session

db_session = connect_to_db()
Base.query = db_session.query_property()

# テーブル定義
class Wine(Base):
  __tablename__ = 'youtube_playlist'
  id = Column(Integer,primary_key=True)
  video_id = Column(Integer,unique=True)
  title = Column(String(255))

  def __init__(self,video_id=None,title=None):
    self.video_id = video_id
    self.title = title

# DB作成
def create_db(new_data):
  Base.metadata.create_all(bind=engine)
  read_data(new_data)

# テーブル作成 - 新規 -
def read_data(new_data)->list:
  for i,index in enumerate(new_data,start=1):
    row = Wine(
      video_id=index[0],
      title=index[1]
    )

    db_session.add(row)
  db_session.commit()

# リストに増減があったら感知
def detect_diff(new_data_):
  db_data = db_session.query(Wine).all()
  db_data = [(k.video_id,k.title) for k in db_data]
  diff_data = list(set(new_data_) ^ set(db_data))
  if diff_data:
    return dealing_db()

# 最新のリストの増減に応じてDBリストのCDを行う
def dealing_db():
  db_data = db_session.query(Wine).all()
  db_data = [(k.video_id,k.title) for k in db_data]
  diff_data = list(set(new_data) ^ set(db_data))
  if len(list(set(new_data) ^ set(db_data))):
    diff_minus = list(set(diff_data) & set(db_data))
    diff_plus = list(set(diff_minus) ^ set(diff_data))
  else:
    pass
  if diff_minus:
    for i in diff_minus:
      db_session.query(Wine).filter(Wine.video_id==i[0]).delete()
    db_session.commit()
  else:
    pass
  if diff_plus:
    for i in diff_plus:
      Wine().video_id = i[0]
      Wine().title = i[1]
      db_session.add(Wine())
    db_session.commit()
  else:
    pass
