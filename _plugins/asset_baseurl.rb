# Markdown files reference images as plain "/assets/..." paths so they also
# display in GitHub's file preview. When the site is built with a baseurl
# (e.g. /discerninglearning on GitHub Pages), prefix those paths with it.
Jekyll::Hooks.register [:pages, :documents], :post_render do |item|
  baseurl = item.site.config["baseurl"].to_s.chomp("/")
  next if baseurl.empty? || item.output.nil?

  item.output = item.output.gsub(/(src|href)="\/assets\//, "\\1=\"#{baseurl}/assets/")
end
