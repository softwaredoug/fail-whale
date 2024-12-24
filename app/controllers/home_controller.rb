class HomeController < ApplicationController
  def index
    template_file = Rails.root.join("app/views/home/index.html.liquid")
    puts "User signed in on devise? #{user_signed_in?}"
    @content = LiquidRenderer.new.render_liquid(template_file, {
        "user_signed_in" => user_signed_in?,
        "current_user_email" => current_user&.email,
        "destroy_user_session_path" => destroy_user_session_path,
        "new_user_registration_path" => new_user_registration_path,
        "new_user_session_path" => new_user_session_path
    })
    render html: @content.html_safe
  end
end
