require "test_helper"

class FeedControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get feed_index_url
    assert_response :success
  end
end
