class FeedController < ApplicationController
  def initialize
    @offset = 0
    super
  end

  def index
    # Loald 10 most recent updated posts from posts table
    @posts = Post.order(updated_at: :desc).limit(10)
    @offset = params[:offset] || 0
    puts "Offset: #{@offset}"
    @next_offset = @offset.to_i + 10
  end
end
