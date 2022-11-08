

class Minesweeper:



    def _init_board(self,size:int,no_bombs:int=-1):
        # if bomb is -1 then =size
        # only initiate matrix and set init parms
        pass
        

    def _generate_board(self,first_dig:tuple):
        # spawn bomb and assign value at same time
        #spawn bomb with low probability near first dig
        # called after first dig

        # matrix contain tuple(has_dug,neigh_bombs)
        # if crr loc is bomb then tuple=tuple(has_flaged,bomb_color_index)

        self.dig(first_dig)
        pass

    def _dig(self,loc):
        # dig at that location!
        # return True if successful dig, False if bomb dug

        # a couple of scenarios to consider:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors!
        pass

    def play(self,dig_loc):
        #max dig = size*size -no_bombs

        # return (game_state , board_matrix)
        pass
