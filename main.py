"""
Platformer Game
"""
import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import PlayerCharacter

SCREEN_TITLE = "Better than Super Mario: SUPER MÜLLER "

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

RESPAWN_X = 64 
RESPAWN_Y = 200 

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_PLAYERSTART = "PlayerStart"
LAYER_NAME_MOVING_PLATFORM = "Moving Platform"
LAYER_NAME_LADDERS = "Ladders"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):

        # Call the parent class and set up the window
        super().__init__(width, height, title, fullscreen=True)

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Our Scene Object
        self.scene = None

        self.life_image = arcade.Sprite(":resources:images/pinball/bumper.png", scale=0.5)

        self.empty_life_image = arcade.Sprite(":resources:images/pinball/pool_cue_ball.png")

        # Separate variable that holds the player sprite
        self.player_sprite = PlayerCharacter()

        # Initializing the coins to be able to count and collect them 
        self.coins = 0

        #TileMap Object
        self.tile_map = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Keep track of the lives 
        self.player_lives = 3

        #set game over to false to be able to play 
        self.game_over = False 

        #Where is the right edge of the map 
        self.end_of_map = 0

        #Make sure the score starts at 0 every time the game starts 
        self.reset_score = True 

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("coin_c_02-102844.mp3")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over_sound = arcade.load_sound("videogame-death-sound-43894.mp3")
        self.lost_live_sound = arcade.load_sound("080205_life-lost-game-over-89697.mp3")
        self.game_won_sound = arcade.load_sound("tada-fanfare-a-6313.mp3")
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.close_window_delayed = False

    def on_resize(self, width, height):
        """Handle window resizing."""
        super().on_resize(width, height)

        # Adjust your game's logic for the new window size here
        # For example, you can update the camera's viewport size
        self.camera.resize(width, height)


    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Game Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.score = 0

        #keep track of the lives 
        self.player_lives = 3

        self.game_over = False

        self.game_won = False

        # Initialize a timer variable (in seconds)
        self.timer = 0.0
        
        # Boolean flag to track if the timer should be running
        self.timer_running = False

        # Initialize Scene
        self.scene = arcade.Scene()
        map_name = "C:/Users/cemuller/Documents/tiled_testing.tmx"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection. True = non moving objects, False = moving objects 

        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORM: {
                "use_spatial_hash": False,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {"use_spatial_hash": True
            },
            LAYER_NAME_PLAYERSTART: {
                "use_spatial_hash": False,
            },}
        
        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

         # Set up the player, specifically placing it at these coordinates.
         # In this case the sprite with it's animations is defined in another Class "PlayerCharacter" in the player.py file 
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = RESPAWN_X
        self.player_sprite.center_y = RESPAWN_Y
        self.scene.add_sprite("Player", self.player_sprite)
        
        # Count the total number of coins in the "Coins" layer
        coins_layer = self.scene[LAYER_NAME_COINS]
        self.coins = len(coins_layer.sprite_list)

        
        if self.reset_score:
            self.score = 0
        self.reset_score = True 
        
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

#this is a manual way to implement the game environment. Usually working with Tiled is faster and more efficient 
            """ # Create the ground
                # This shows using a loop to place multiple sprites horizontally
                for x in range(0, 1250, 64):
                    wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
                    wall.center_x = x
                    wall.center_y = 32
                    self.scene.add_sprite("Walls", wall)
        

                # Put some crates on the ground
                # This shows using a coordinate list to place sprites
                coordinate_list = [[512, 96], [256, 120], [400, 270], [768, 96], [850, 250], [1000, 370],[1400, 80],[1550, 140], [1750, 240], [1930, 400], [2120, 550], [1930, 700], [1790, 880], [1500, 680], [1300, 500]]

                for coordinate in coordinate_list:
                # Add a crate on the ground
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
                    wall.position = coordinate
                    self.scene.add_sprite("Walls", wall)

                    # Calculate the y coordinate for the coins based on crate height
                    crate_height = wall.height
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
                    coin.center_x = wall.center_x
                    coin.center_y = wall.center_y + crate_height // 2 + 50  # Adjust 10 as needed
                    self.scene.add_sprite("Coins", coin)
                    self.coins += 1
            """


        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, ladders=self.scene[LAYER_NAME_LADDERS], platforms=self.scene[LAYER_NAME_MOVING_PLATFORM], gravity_constant=GRAVITY, walls=self.scene["Platforms"])


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()


        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

         # Display the timer
        rounded_timer = round(self.timer, 2)
        timer_text = f"Time: {float(rounded_timer)} "
        arcade.draw_text(
        
        timer_text,
        10,
        160, 
        arcade.csscolor.WHITE,
        18,
    )

        # Draw our lives on the screen, scrolling it with the viewport

        #draw the images for the lives 
        for i in range(self.player_lives):
            x = 30 + i * (self.life_image.width + 5)  # Adjust the scaling factor as needed
            y = 120
            self.life_image.center_x = x
            self.life_image.center_y = y
            self.life_image.draw()

        # draw text with number of lives left 
        lives_text = f"Lives: {self.player_lives}"
        arcade.draw_text(
            
            lives_text,
            10,
            70,
            arcade.csscolor.WHITE,
            18,

        )

        # Display the initial coin count
        coin_count_text = f"Coins left: {self.coins}"
        arcade.draw_text(
            
            coin_count_text,
            10,
            40,
            arcade.csscolor.WHITE,
            18,
        )

        # Draw our score on the screen, scrolling it with the viewport

        score_text = f"Score: {self.score}"

        arcade.draw_text(

            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,

        )

        # check if conditions for game over or game won are given and operate properly 
        if self.game_over:
            self.timer_running = False
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.BLACK, 54, anchor_x="center")
            arcade.draw_text(f"Time: {rounded_timer}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, arcade.color.BLACK, 54, anchor_x="center")
        if self.coins == 0:
            arcade.draw_text("CONGRATS!!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.BLACK, 54, anchor_x="center")
            arcade.draw_text(f"Time: {rounded_timer}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, arcade.color.BLACK, 54, anchor_x="center")

            arcade.play_sound(self.game_won_sound)

    def process_keychange(self): 
        """
        Called when we change a key up/down or we move on/off a ladder.
        """

        # Process up/down movement
        if self.up_pressed and not self.down_pressed:
            # Check if the player is on a ladder
            if self.physics_engine.is_on_ladder():
                # Move the player upwards on the ladder
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            # Check if the player can jump and hasn't recently jumped
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                # Make the player jump and mark jump as reset
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                # Play a jump sound
                arcade.play_sound(self.jump_sound)
        # Process downward movement
        elif self.down_pressed and not self.up_pressed:
            # Check if the player is on a ladder
            if self.physics_engine.is_on_ladder():
                # Move the player downwards on the ladder
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder with no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                # Stop vertical movement when no keys are pressed
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                # Stop vertical movement when both up and down keys are pressed
                self.player_sprite.change_y = 0

        # Process left/right movement
        if self.right_pressed and not self.left_pressed:
            # Move the player to the right
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            # Move the player to the left
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            # Stop horizontal movement when no keys are pressed
            self.player_sprite.change_x = 0



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

        if key == arcade.key.F or key == arcade.key.S:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        # Check if the game is over or the game is won
        if self.game_over or self.game_won:
            return

        # Check which key was released and update corresponding pressed status
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        # Process key change to adjust player movement
        self.process_keychange()

    def center_camera_to_player(self):
        """
        Center the camera on the player character.
        """
        # Calculate the screen center based on player's position and camera viewport
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Ensure the screen center doesn't go below 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Create a tuple with the centered coordinates
        player_centered = screen_center_x, screen_center_y

        # Move the camera to focus on the player
        self.camera.move_to(player_centered)



    def respawn_character(self):
        self.player_sprite.center_x = RESPAWN_X
        self.player_sprite.center_y = RESPAWN_Y

    def lose_live(self):
        self.player_lives -= 1 
        arcade.play_sound(self.lost_live_sound)
        if self.player_lives <1: 
            self.player_lives = 0
            self.game_over = True
            arcade.play_sound(self.game_over_sound)
            
        else: 
            self.respawn_character()

    def close_window(self, delta_time):
        arcade.close_window()

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations for the player character
        self.player_sprite.update_animation(delta_time)

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        # Update Animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS]
        )
        self.scene.update([LAYER_NAME_MOVING_PLATFORM])

         # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_COINS]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Subtract one from the coin count
            self.coins -= 1
            self.score += 1 
            # Check if this is the first coin collected and start the timer
            if not self.timer_running:
                self.timer_running = True

        if self.timer_running:
            self.timer += delta_time  # Increment the timer by the time that has passed

        # Check for win condition
        if self.coins == 0:
            self.timer_running = False
            if not self.close_window_delayed:
                arcade.schedule(self.close_window, 5.0)  # Schedule the window to close in 5 seconds
                self.close_window_delayed = True
            

        # Check if player fell out of the screen
        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = RESPAWN_X
            self.player_sprite.center_y = RESPAWN_Y
            self.lose_live()

        # Check if player's vertical velocity exceeds a threshold
        if self.player_sprite.change_y <= -40:
            self.lose_live()

        # Position the camera
        self.center_camera_to_player()

        # Check for win condition
        if self.game_won:
            if not self.close_window_delayed:
                arcade.schedule(self.close_window, 5.0)  # Schedule the window to close in 5 seconds
                self.close_window_delayed = True

        # Check for loss condition
        if self.game_over:
            if not self.close_window_delayed:
                arcade.schedule(self.close_window, 5.0)  # Schedule the window to close in 5 seconds
                self.close_window_delayed = True


def main():
    """Main function"""
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()