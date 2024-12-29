require "test_helper"
require "minitest/mock"

class FeedControllerTest < ActionDispatch::IntegrationTest
  setup do
    tweets = []
    (0..10).each do |i|
      tweets.push({ content: "Tweet #{i}", username: "@user#{i}" })
    end
  end
  test "should get index" do
    get posts_path
    assert_response :success
  end
end
