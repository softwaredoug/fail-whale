
class LiquidRenderer
  def render_liquid(template_path, assigns = {})
    template = File.read(template_path)
    Liquid::Template.parse(template).render(assigns.stringify_keys)
  end
end
