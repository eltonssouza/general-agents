# Example with constructs that the R30-R34 notes address (checker fixture; not code to be executed)
require "set"

OldPoint = Struct.new(:x, :y)

def process_text(input)
  buffer = "Result: "
  buffer << input

  if File.exists?("/tmp/x") && defined?(Fixnum)
    puts "legacy"
  end

  # back-reference: the note says the optimization does not cover this case
  repeated = /^(a+)\1$/ =~ input

  YAML.load(input)
  Timeout.timeout(-1) { sleep 1 }
  [1, 2].map { it * 2 }
  IO.select([$stdin])
end
