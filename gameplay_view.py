import arcade 

class GameplayView(arcade.View):

    def __init__(self, player_sprite, coins, tile_map, physics_engine, camera, gui_camera, score, player_lives, game_over, game_won, timer, timer_running, close_window_delayed):
        super().__init__()

        self.player_sprite = player_sprite
        self.coins = coins
        self.tile_map = tile_map
        self.physics_engine = physics_engine
        self.camera = camera
        self.gui_camera = gui_camera
        self.score = score
        self.player_lives = player_lives
        self.game_over = game_over
        self.game_won = game_won
        self.timer = timer
        self.timer_running = timer_running
        self.close_window_delayed = close_window_delayed
        
    def on_show(self):
        return super().on_show()
    
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
