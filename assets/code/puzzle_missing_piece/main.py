import replicate

def generate_image(prompt: str) -> any:
  output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={"prompt": "an iguana on the beach, pointillism"}
  )
  return output

def load_image(image: any) -> any:
  # Identify the image
  image = open(image, "rb")
  # or...
  #image = "https://example.com/mystery.jpg"

  output = replicate.run(
    "replicate/resnet:dd782a3d531b61af491d1026434392e8afb40bfb53b8af35f727e80661489767",
    input={"image": image}
  )
  return output

def create_the_missing_part(image: any) -> any:
  # Doesn't work with picture without a face - https://github.com/orpatashnik/StyleCLIP/issues/66
  image = open(image, "rb")

  output = replicate.run(
    "adirik/stylemc:708f7bca82339e47999c6dcec9bae35e134997dc7cfa40108eea4e4f0defcfe7",
    input = {
      "image": image,
      "custom_prompt": "Create the missing part of the image."
    }
  )
  return output

def create_the_missing_puzzle_piece(image: any) -> any:
  # https://replicate.com/timothybrooks/instruct-pix2pix?input=python
  # https://github.com/chenxwh/cog-themed-diffusion/tree/instruct_pix2pix?tab=readme-ov-file
  image = open(image, "rb")
  output = replicate.run(
    "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
    input={
        "image": image,
        "prompt": "generate the missing puzzle piece",
        "scheduler": "K_EULER_ANCESTRAL",
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "num_inference_steps": 100,
        "image_guidance_scale": 1.5
    }
  )
  return output
  
if __name__ == "__main__":
  # prompt = "an iguana on the beach, pointillism"
  # image = generate_image(prompt)
  # print(image)
  # print(load_image("IMG_20240106_191844.png"))
  
  # print(create_the_missing_part("./IMG_20240106_191844.png"))
  print(create_the_missing_puzzle_piece("./IMG_20240106_191844.png"))