from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

WEIGHT = {"Easy": 1, "Medium": 2, "Hard": 3}

@dataclass(frozen=True)
class Block:
    kind: str
    title: str
    subject: str
    start: datetime
    end: datetime
    task_id: int | None

    @property
    def minutes(self):
        return int((self.end - self.start).total_seconds() // 60)

class SmartScheduler:
    def __init__(self, day=None, start=time(17,0), end=time(22,0), block=45, break_min=15):
        self.day = day or date.today(); self.start=start; self.end=end
        self.block=max(15, block); self.break_min=max(5, break_min)

    def generate(self, tasks):
        pending=[t for t in tasks if not t.completed and t.minutes > 0]
        pending.sort(key=lambda t: ((date.fromisoformat(t.deadline)-self.day).days, -WEIGHT.get(t.difficulty,2), -t.minutes, t.id))
        cur=datetime.combine(self.day,self.start); end=datetime.combine(self.day,self.end); result=[]
        for task in pending:
            left=task.minutes
            while left and cur<end:
                available=int((end-cur).total_seconds()//60)
                chunk=min(self.block,left,available)
                if chunk<=0: break
                stop=cur+timedelta(minutes=chunk)
                result.append(Block("study", task.name, task.subject, cur, stop, task.id))
                left-=chunk; cur=stop
                if cur<end and left>0 or (cur<end and task is not pending[-1]):
                    b=min(self.break_min,int((end-cur).total_seconds()//60))
                    if b>0:
                        stop=cur+timedelta(minutes=b); result.append(Block("break","Break","",cur,stop,None)); cur=stop
        return result
