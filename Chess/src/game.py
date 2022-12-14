
import pygame
from src.vector2 import Vector2
from src.board_piece import BoardPiece
from src.pawn import Pawn

class Game:
	square_size = 75
	grid_pos = Vector2(10, 10)

	# colours for squares
	board_colours = [
		(240, 230, 200), # light
		(200, 170, 120), # dark
		(255, 245, 215), # light hover - old
		(215, 185, 135), # dark hover - old
		(255, 250, 225), # light hover
		(235, 195, 145), # dark hover
	]

	def __init__(self):
		self.run = True
		self.window = pygame.display.set_mode((620, 620))
		self.is_player1_turn = True
		self.active_sprite = None
		self.highlight_moves = []

		self.white_player = [
			BoardPiece(Vector2(3, 7), "./sprites/white/queen.png"),
			BoardPiece(Vector2(4, 7), "./sprites/white/king.png"),
			*[BoardPiece(Vector2(i, 7), "./sprites/white/rook.png") for i in (0, 7)],
			*[BoardPiece(Vector2(i, 7), "./sprites/white/bishop.png") for i in (1, 6)],
			*[BoardPiece(Vector2(i, 7), "./sprites/white/knight.png") for i in (2, 5)],
			*[Pawn(Vector2(i, 6), "./sprites/white/pawn.png") for i in range(8)]
		]
	
		self.black_player = [
			BoardPiece(Vector2(3, 0), "./sprites/black/queen.png"),
			BoardPiece(Vector2(4, 0), "./sprites/black/king.png"),
			*[BoardPiece(Vector2(i, 0), "./sprites/black/rook.png") for i in (0, 7)],
			*[BoardPiece(Vector2(i, 0), "./sprites/black/bishop.png") for i in (1, 6)],
			*[BoardPiece(Vector2(i, 0), "./sprites/black/knight.png") for i in (2, 5)],
			*[Pawn(Vector2(i, 1), "./sprites/black/pawn.png", white=False) for i in range(8)]
		]

	# handle events and input
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False

			if event.type == pygame.MOUSEBUTTONDOWN:

				# check if player is moving a sprite
				if self.active_sprite != None:
					for move in self.highlight_moves:
						move_pos = Game.grid_pos + move * Vector2(75,75)
						if pygame.Rect(move_pos.x, move_pos.y, Game.square_size, Game.square_size).collidepoint(event.pos):

							# get active sprite
							for sprite_list in (self.white_player, self.black_player):
								for sprite in sprite_list:
									if id(sprite) == self.active_sprite:

										# move the sprite
										sprite.move_to(move)
										self.is_player1_turn = not self.is_player1_turn
										self.active_sprite = None
										self.highlight_moves = []
										return


				# check if player has clicked a sprite
				for sprite_list in (self.white_player, self.black_player):
					for sprite in sprite_list:
						sprite_pos = Game.grid_pos + sprite.pos * Vector2(75,75)
						
						if pygame.Rect(sprite_pos.x, sprite_pos.y, Game.square_size, Game.square_size).collidepoint(event.pos):
							
							# set or remove as active sprite
							self.active_sprite = id(sprite) if self.active_sprite != id(sprite) else None
							
							# get highlighted squares for active sprite
							self.highlight_moves = []
							for sprite_list in (self.white_player, self.black_player):
								for sprite in sprite_list:
									if self.active_sprite == id(sprite):
										self.highlight_moves = sprite.get_moves(self)

	# draw game board
	def draw_grid(self) -> None:

		# copy to local object
		square_pos = Game.grid_pos.get_copy()

		# iterate through grid
		for y in range(8):
			for x in range(8):

				# get base square colour
				is_dark_square = (x+y) % 2
				is_highlighted_square = False

				# get bound of square
				square_rect = (square_pos.x, square_pos.y, Game.square_size, Game.square_size)
			
				# use highlighted colour if mouse is over current square
				if pygame.Rect(square_rect).collidepoint(*pygame.mouse.get_pos()):
					is_highlighted_square = True

				# use highlighted colour if the active sprite can move to this square
				if Vector2(x,y) in self.highlight_moves:
					is_highlighted_square = True

				# draw square
				pygame.draw.rect(self.window, self.board_colours[is_dark_square + is_highlighted_square*2], square_rect)
				if is_highlighted_square:
					pygame.draw.rect(self.window, (0,0,0), square_rect, 1)

				# increment to next square
				square_pos.x += Game.square_size
			
			# move to start of next row
			square_pos.x -= Game.square_size * 8
			square_pos.y += Game.square_size

			
	# draw all sprites
	def draw_sprites(self) -> None:
		for sprite_list in (self.white_player, self.black_player):
			for sprite in sprite_list:
				pos = Game.grid_pos + sprite.pos * Vector2(Game.square_size, Game.square_size)
				self.window.blit(sprite.surface, pos.get_tuple())
				

	# get piece at position
	def get_from_posision(self, target_pos: Vector2):
		for sprite_list in (self.white_player, self.black_player):
			for sprite in sprite_list:
				if sprite.pos == target_pos:
					return sprite
		return None

