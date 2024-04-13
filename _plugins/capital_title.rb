module Jekyll
  module Utils
    def titleize_slug(slug)
      words_to_capitalize = ['llm']
      slug.split(/[_-]/).map do |word|
        words_to_capitalize.include?(word) ? word.capitalize : word
      end.join(' ')
    end
  end
end
