import arcade

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1
CHARACTER_SCALING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):
        # Call the constructor of the parent class (arcade.Sprite)
        super().__init__()

        # Default to facing right
        self.character_face_direction = RIGHT_FACING

        # Used to switch between different animation frames
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track player state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # Load Textures

        # Define the base path for character textures
        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture to idle facing right
        self.texture = self.idle_texture_pair[0]

        # Define the hit box based on the initial texture
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        # Flip the character based on movement direction
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True

        # Check if the character was climbing but is no longer on a ladder
        if not self.is_on_ladder and self.climbing:
            self.climbing = False

        # Check if character is actively climbing and moving vertically
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1

            # Loop the climbing animation if it reaches the end
            if self.cur_texture > 7:
                self.cur_texture = 0

        # Set the texture to the appropriate climbing frame
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1

        # Loop the walking animation if it reaches the end
        if self.cur_texture > 7:
            self.cur_texture = 0

        # Set the texture to the appropriate walking frame
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
