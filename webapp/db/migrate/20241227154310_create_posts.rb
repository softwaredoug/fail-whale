class CreatePosts < ActiveRecord::Migration[8.0]
  def change
    create_table :posts do |t|
      t.string :content
      t.string :username

      t.timestamps
    end
  end
end
