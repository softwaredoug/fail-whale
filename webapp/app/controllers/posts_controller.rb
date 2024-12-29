class PostsController < ApplicationController
  def initialize
    @limit = 10
    @user_post = Post.new
    super
  end

  def new
    @user_post = Post.new
  end

  def create
    @post = Post.new(post_params)
    if @post.save
      redirect_to posts_path(limit: @limit)
    else
      flash.now[:alert] = "Failed to share post."
      render "index"
    end
  end

  def index
    # Loald 10 most recent updated posts from posts table
    @limit = params[:limit].to_i || 10
    if @limit < 10
      @limit = 10
    end
    @posts = Post.order(updated_at: :desc).limit(@limit)
    @next_limit = @limit + 10
  end

  private

  def post_params
    username = "softwaredoug"
    w_content = params.require(:post).permit(:content)
    w_content[:username] = username
    w_content
  end
end
