require "test_helper"
require "minitest/mock"

class FeedControllerTest < ActionDispatch::IntegrationTest
  setup do
    tweets = []
    (0..10).each do |i|
      tweets.push({ content: "Tweet #{i}", username: "@user#{i}" })
    end
    @mock_chatgpt = Minitest::Mock.new
    @mock_chatgpt.expect(:tweets, tweets, [ 10 ])
  end
  test "should get index" do
    Chatgpt.stub(:new, @mock_chatgpt) do
      get feed_index_url
      assert_response :success
    end
  end
end
