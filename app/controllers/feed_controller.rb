class FeedController < ApplicationController
  def index
    @posts = [
      { content: "Hello, world!" },
      { content: "Goodbye, world!" }
    ]
  end
end
