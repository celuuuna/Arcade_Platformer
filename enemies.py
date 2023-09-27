import arcade 
CHARACTER_SCALING = 1
# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.character_face_direction = RIGHT_FACING

        main_path = f":resources:images/enemies/{name_file}"

        self.bee_texture_pair = load_texture_pair(f"{main_path}_bee.png")
        self.wormPink_texture_pair = load_texture_pair(f"{main_path}_wormPink.png")
        self.slimeBlue_texture_pair = load_texture_pair(f"{main_path}_slimeBlue.png")

        

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

