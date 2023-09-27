import arcade 

class GameoverView (arcade.View):
    def on_show(self):
        return super().on_show()
    
    def on_draw(self):
        return super().on_draw()
    
    def on_key_press(self, key, modfiers):
        # Handle key presses on the game over screen
        if key == arcade.key.ENTER:
            # Transition to the title view
            title_view = TitleView()
            self.window.show_view(title_view)