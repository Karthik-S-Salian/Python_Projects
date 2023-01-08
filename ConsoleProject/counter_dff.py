from time import sleep

class FlipFlop:
    def __init__(self,reset:bool,clear:bool):
        self.output_state:bool=clear
        self.reset:bool=reset
        self.clear:bool=clear
        
    def set_reset(self,state:bool):
        self.reset:bool=state
        if reset:
            self.output_state=0
        
    def set_clear(self,state):
        self.clear:bool=state
        if clear:
            self.output_state=1
      
    def get_output_state(self)->bool:
        return self.output_state
        
        
class D_FlipFlop(FlipFlop):
    def __init__(self,reset=0,clear=0):
        super().__init__(reset,clear)
        
    def on_clock_update(self,D_state:bool)->bool:
        self.output_state=D_state
        return self.output_state
        

if __name__=="__main__":
    dff_list=[D_FlipFlop() for _ in range(4)]
    q_list=[0,0,0,0]
    while True:
        for i,dff in enumerate(dff_list):
            q_list[i]=dff.get_output_state()
        
        
        d0=not q_list[0]
        d1=(not(q_list[0] or q_list[1])) or (q_list[0] and q_list[1]) and (q_list[3] or q_list[2])
        d2=(not(q_list[0] or q_list[1] or q_list[2])) or (not q_list[3]) and (q_list[1] or q_list[0])
        d3=(not(q_list[3] or q_list[2])) or (q_list[3]) and (q_list[1] or q_list[0] or q_list[2])
        dff_list[0].on_clock_update(d0)
        dff_list[1].on_clock_update(d1)
        dff_list[2].on_clock_update(d2)
        dff_list[3].on_clock_update(d3)
        
        weight=1
        num=0
        for q in q_list:
            num+=q*weight
            weight=weight*2
        print(int(num))
        sleep(1)
        
    
    