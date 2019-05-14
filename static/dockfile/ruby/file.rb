

hash = Hash.new 
hash = { :water => 'wet', :fire => 'hot' }
                                         
puts hash[:fire] 

hash.each_pair do |key, value|  
  puts "#{key} is #{value}"
end

hash.delete :water                            
hash.delete_if {|key,value| value == 'hot'}  


print(hash)