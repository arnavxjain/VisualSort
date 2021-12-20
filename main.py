import pygame
import random
import math

pygame.init()

class DrawInfo:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 24, 254, 122
	BLUE = 60, 20, 180
	YELLOW = 254, 222, 58
	RED = 255, 0, 0
	GREY = 128, 128, 128
	BG = BLACK

	GRADIENTS = [
		(234, 104, 170),
		(143, 101, 187),
		(57, 98, 203)
	]

	BLUE_GRADIENT = [
		(73, 73, 255),
		(120, 121, 255),
		(163, 163, 255)
	]

	myfont = pygame.font.Font("Poppins-Medium.ttf", 20)

	SIDE_PADDING = 100
	TOP_PADDING = 150

	def __init__(self, width, height, lst):
		self.height = height
		self.width = width

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm")
		self.set_LST(lst)

	def set_LST(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PADDING) / len(lst))

		self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))

		self.start_x = self.SIDE_PADDING // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BG)

	title = draw_info.myfont.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 12)) 
 
	controls = draw_info.myfont.render("R : Reset | A : Ascending | D : Dsecending | Space : Initialize Sort", 1, draw_info.WHITE)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 40)) 

	sorting = draw_info.myfont.render("I : Insertion Sort | B : Bubble Sort", 1, draw_info.WHITE)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 70)) 

	draw_list(draw_info)

	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_BG=False):
	lst = draw_info.lst

	if clear_BG:
		clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)

		pygame.draw.rect(draw_info.window, draw_info.BG, clear_rect)


	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.BLUE_GRADIENT[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_BG:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

def bubble(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i -1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def main():
	run = True
	clock = pygame.time.Clock()

	lst = generate_starting_list(50, 0, 100)
	draw_info = DrawInfo(800, 600, lst)

	sorting = False
	ascending = True	

	sorting_algo = bubble
	sorting_header = "Bubble Sort"
	sorting_algo_generator = None
	
	while run:
		clock.tick(120)

		if sorting:
			try:
				next(sorting_algo_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_header, ascending)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(50, 0, 100)
				draw_info.set_LST(lst)
				sorting = False

			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algo_generator = sorting_algo(draw_info, ascending)


			elif event.key == pygame.K_a and not sorting:
				# sorting = True
				ascending = True

			elif event.key == pygame.K_d and not sorting:
				sorting = False
				ascending = False


			elif event.key == pygame.K_i and not sorting:
				sorting_algo = insertion
				sorting_header = "Insertion Sort"

			elif event.key == pygame.K_b and not sorting:
				sorting_algo = bubble
				sorting_header = "Bubble Sort"


	pygame.quit()


if __name__ == "__main__":
	main()