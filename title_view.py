import arcade 

class TitleView(arcade.View):
    
    def on_show(self):
        return super().on_show()

    def on_draw(self):
        return super().on_draw()

    def on_key_press(self, key, modifiers):
        # Handle key presses on the title screen
        if key == arcade.key.ENTER:
            # Transition to the gameplay view
            gameplay_view = GameplayView()
            self.window.show_view(gameplay_view)
        elif key == arcade.key.I:
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)