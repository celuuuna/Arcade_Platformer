import arcade 

class GamewonView (arcade.View):
    def on_show(self):
        return super().on_show()
    
    def on_draw(self):
        return super().on_draw()
    
    def on_key_press(self, key, modifiers):
        # Handle key presses on the game won screen
        if key == arcade.key.ENTER:
            # Transition to the title view
            title_view = TitleView()
            self.window.show_view(title_view)