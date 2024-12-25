class FeedController < ApplicationController
  def initialize
    @chatgpt = Chatgpt.new
    @offset = 0
    super
  end

  def index
    @posts = @chatgpt.tweets(5)
    puts "Offset: #{@offset}"
    @next_offset = @offset.to_i + 10
  end
end
