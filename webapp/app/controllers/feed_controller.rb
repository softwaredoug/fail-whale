class FeedController < ApplicationController
  def initialize
    @chatgpt = Chatgpt.new
    @offset = 0
    super
  end

  def index
    @offset = params[:offset] || 0
    @posts = @chatgpt.tweets(10 + @offset.to_i)
    puts "Offset: #{@offset}"
    @next_offset = @offset.to_i + 10
  end
end
