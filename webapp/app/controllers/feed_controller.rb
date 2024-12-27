class FeedController < ApplicationController
  def initialize
    @limit = 10
    super
  end

  def index
    # Loald 10 most recent updated posts from posts table
    @limit = params[:limit].to_i || 10
    @posts = Post.order(updated_at: :desc).limit(@limit)
    @next_limit = @limit + 10
  end
end
