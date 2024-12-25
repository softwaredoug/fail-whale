class FeedController < ApplicationController
  def index
    @offset = params[:offset] || 10
    @posts = []
    puts "Offset: #{@offset}"
    @offset.to_i.times do |i|
      @posts.push({ user: "user#{i}", content: "This is post number #{i}",
                    scroll_posn: i })
    end
  @next_offset = @offset.to_i + 10
  end
end
