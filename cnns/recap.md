# Convolutional networks — recap & real-world examples

*Part of [Convolutional networks for the product and technology leader](./README.md)*

## Real-world examples & war stories

These are documented facts from the sources, not incidents. Where a story is invented to show a failure, it says so.

**Weight sharing cut a layer's size by about 3,000 times.** The CS231n course notes work through the first layer of AlexNet. Without weight sharing it would need 105,705,600 parameters. With one shared kernel per output channel it needs 34,944. 🎯 *Takeaway:* a convolution's power is that it reuses a few weights everywhere, so parameters are cheap and compute is not. Price resolution, not parameters. This is [lesson 2](./how-a-convolution-sees.md).

**Skip connections and the 2015 ImageNet challenge.** The CS231n notes record that ResNet, from Kaiming He and colleagues, won the ILSVRC 2015 challenge, and that it relies on skip connections. Torchvision's code still builds every ResNet block around one line, `out += identity`. 🎯 *Takeaway:* a residual block can pass its input through and add a correction on top. Depth still costs latency. When a team proposes a deeper backbone, ask whether the gain pays for the latency. This is [lesson 3](./from-edges-to-objects.md).

**Zero-shot matched a supervised baseline, and the vendor still said "not for deployment".** OpenAI's CLIP README reports that CLIP matches the original ResNet-50 on ImageNet zero-shot, without using its 1.28 million labelled examples. The CLIP model card also says that "any deployed use case of the model … is currently out of scope." 🎯 *Takeaway:* capability and permission are separate questions. Read the model card and the licence before the prototype becomes the plan. This is [lesson 6](./vision-foundation-models.md).

**Benchmarks built to break clean scores.** The ImageNet-C benchmark applies 15 corruption types to ImageNet images. Its authors also point to ImageNet-A, natural images "that cause model accuracy to substantially degrade." 🎯 *Takeaway:* one clean test set does not predict behaviour on real cameras. Score corrupted copies of your own images. This is [lesson 7](./shipping-vision-in-production.md).

**An 8-bit model trades accuracy for speed.** TensorFlow's MobileNet page lists MobileNetV3-Large on a Pixel 1 phone at 51.2 ms in float and 44 ms in 8-bit, with ImageNet top-1 of 75.2% and 73.9%. 🎯 *Takeaway:* lower precision is a priced tradeoff, not a free speed-up. Test it on your images. This is [lesson 7](./shipping-vision-in-production.md).

**The camera that swapped red and blue (an illustration).** A warehouse adds new cameras that deliver blue-green-red images. The serving code assumes red-green-blue. Accuracy falls, while latency and error rates look normal. A test comparing training and serving inputs would have caught it before launch. The story is invented. 🎯 *Takeaway:* treat preprocessing as a contract with a test.

**The detector that should have been a classifier (an illustration).** A team spends months drawing boxes for a shelf monitor whose only product question is "does this shelf need restocking?" A three-way classifier would have needed a few hours of labelling. The story is invented, and the [labelling arithmetic is in lesson 1](./what-computer-vision-does.md). 🎯 *Takeaway:* pick the least detailed output that answers the product question.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What computer vision does](./what-computer-vision-does.md) | Four jobs: classify, detect, segment, embed. Each step adds detail and labelling cost. | What is the simplest output that answers our product question? |
| [How a convolution sees](./how-a-convolution-sees.md) | One small kernel, shared across the image. Few weights, compute that grows with the pixel count. | What resolution do we need, and what does doubling it cost? |
| [From edges to objects](./from-edges-to-objects.md) | Depth grows the receptive field. Early features are generic, late ones specific. | Which layer are we reusing, and did we compare it with an earlier one? |
| [Transfer learning and labels](./transfer-learning-and-labels.md) | Start from a pre-trained model. How you reuse it depends on data size and similarity. | What did a frozen baseline score before we fine-tuned? |
| [CNNs vs. vision transformers](./cnns-vs-vision-transformers.md) | A ViT turns patches into tokens. A CNN builds in locality. Similar accuracy can carry very different compute. | What does each family score and cost on our data, at our resolution? |
| [Vision foundation models](./vision-foundation-models.md) | CLIP, DINO and SAM can need few labels or none. Licences and intended-use notes vary. | Does a foundation model meet the bar, and may we ship it? |
| [Shipping vision in production](./shipping-vision-in-production.md) | Preprocessing, hardware and changing images decide whether it keeps working. | Does a test fail if serving preprocessing differs from training? |

**The through-line:** a vision product is a chain of choices, and each link has a price. The framing sets the labelling bill. Resolution sets the compute bill. The backbone and the foundation model set accuracy, cost and licence terms. The camera and the preprocessing code decide whether any of it survives contact with real images. At every link, the cheapest test is to measure on your own images before you commit.

> **Walk-away question:** *"For our vision feature: what is the simplest output that answers the product question, what resolution and hardware does it need, what did a frozen pre-trained baseline score, may we ship the model we used, and what test catches a preprocessing mismatch?"*

If you can answer all five, you can steer the work. If not, you know which lesson to reread.

## Test yourself

1. **A product team asks for pixel-level masks of every item on a shelf. The product only needs to know when a shelf is nearly empty. What do you suggest, and why?**
   <details><summary>Answer</summary>Start with classification: one label per shelf image, such as full, partly empty or empty. It answers the product question and costs a fraction of the labelling time of masks. Move to detection or segmentation only when the question needs location or area. (<a href="./what-computer-vision-does.md">Lesson 1</a>)</details>
2. **A predicted box and the true box overlap, but the IoU is 0.14. Does it count as a correct detection in COCO-style mAP?**
   <details><summary>Answer</summary>Not at any of the thresholds COCO-style mAP averages over, which run from 0.50 to 0.95. An IoU of 0.14 is below all of them. Touching the object is not enough. (<a href="./what-computer-vision-does.md">Lesson 1</a>)</details>
3. **Engineering wants to double the input side from 224 to 448 pixels to catch small defects. What happens to parameters and to compute in a convolution layer?**
   <details><summary>Answer</summary>The parameters stay the same, because the kernels are shared across positions. The compute per layer rises about four times, because the number of positions quadruples. Activation memory rises about four times too. Price the change before approving it. (<a href="./how-a-convolution-sees.md">Lesson 2</a>)</details>
4. **Torchvision lists ResNet-50 at 4.089 "GFLOPS". TensorFlow's MobileNet page lists MobileNetV3-Large at 217 million MACs. Can you divide one by the other to say how much cheaper MobileNet is?**
   <details><summary>Answer</summary>No, not safely. The labels differ, "GFLOPS" against MACs, yet for MobileNetV3-Large the two sources give the same number: torchvision lists 0.217 "GFLOPS" and the MobileNet page 217 million MACs. So a label may not mean what you assume. Find out how each source counts before you compare or convert. A count that treats a multiply and an add as two FLOPs is twice a MAC count. Then measure latency on your own hardware, which is the number that matters. (<a href="./how-a-convolution-sees.md">Lesson 2</a>)</details>
5. **Your images are X-ray scans, nothing like everyday photos. Your team uses features from the last layer of an ImageNet model and accuracy stalls. What should it try?**
   <details><summary>Answer</summary>Features from an earlier layer. Early layers hold more generic patterns, such as edges, that are useful for many tasks. For a small, very different dataset, the CS231n notes suggest training on activations from earlier in the network. The last layers are tuned to the original dataset's classes. Compare both on a held-out set. (<a href="./from-edges-to-objects.md">Lesson 3</a>)</details>
6. **You have 800 labelled images in 3 classes that look like everyday photos. What is the first model to try?**
   <details><summary>Answer</summary>A frozen pre-trained backbone with a simple linear classifier on its features. With a small, similar dataset, fine-tuning risks overfitting. Fund fine-tuning or more labels only if this baseline misses the bar. (<a href="./transfer-learning-and-labels.md">Lesson 4</a>)</details>
7. **Why can a ViT's cost rise more than a CNN's when you double the image side?**
   <details><summary>Answer</summary>Doubling the side quadruples the number of patches, so the token count rises about four times. Attention scores every token against every token, so that part grows about sixteen times. A convolution layer grows only with the pixel count, about four times. (<a href="./cnns-vs-vision-transformers.md">Lesson 5</a>)</details>
8. **A team wants a ViT trained from scratch on 3,000 images for a phone app. What concerns do you raise?**
   <details><summary>Answer</summary>A ViT lacks a CNN's built-in locality and leans on large pre-training, so training from scratch on 3,000 images is risky. It also costs more compute per image than a small CNN such as MobileNetV3. Start from pre-trained weights, and compare against a mobile CNN on the target phone. (<a href="./cnns-vs-vision-transformers.md">Lesson 5</a>)</details>
9. **A zero-shot CLIP prototype reports 98% probability on most images. Is the model 98% accurate?**
   <details><summary>Answer</summary>No. CLIP's softmax scales small differences in similarity by 100, so it can look very sure while being wrong. Measure accuracy on a labelled test set from your own images, and set a threshold below which a person decides. (<a href="./vision-foundation-models.md">Lesson 6</a>)</details>
10. **Before shipping a feature built on a pre-trained vision model, what two documents do you read?**
    <details><summary>Answer</summary>The licence for the exact weights, and the vendor's intended-use statement or model card. Licences can differ even inside one repository. As of 2026-10, the DINOv2 README releases its main code and weights under Apache License 2.0, and its XRay-DINO and Cell-DINO weights under the FAIR Noncommercial Research License. Some model cards also rule out deployment. (<a href="./vision-foundation-models.md">Lesson 6</a>)</details>
11. **After a camera upgrade, accuracy drops but there are no errors and latency is normal. What do you check first?**
    <details><summary>Answer</summary>The preprocessing contract: colour order, resize and crop, normalisation, orientation and channel layout. Compare the model inputs from the new cameras with the training pipeline's inputs. Then check image statistics such as brightness and blur for a shift. (<a href="./shipping-vision-in-production.md">Lesson 7</a>)</details>
12. **Eight cameras at 10 frames per second, batches of 8, and 20 ms per batch. How many cameras can one GPU serve, as a first estimate?**
    <details><summary>Answer</summary>The GPU can run 1,000 ÷ 20 = 50 batches a second, which is 400 images a second. At 10 frames per second per camera, that is 40 cameras. Confirm with a load test, because latency does not always scale with load. (<a href="./shipping-vision-in-production.md">Lesson 7</a>)</details>

## Sources

- CS231n course notes, *Convolutional Neural Networks* ([GitHub source, master branch](https://github.com/cs231n/cs231n.github.io/blob/master/convolutional-networks.md)): the AlexNet first-layer counts with and without sharing; ResNet as the ILSVRC 2015 winner, with skip connections. Read 2026-10.
- PyTorch torchvision source, `torchvision/models/resnet.py` ([GitHub, main branch](https://github.com/pytorch/vision/blob/main/torchvision/models/resnet.py)): `out += identity` in each block; ResNet-50 `IMAGENET1K_V2` lists `_ops` of 4.089, which torchvision's documentation build (`docs/source/conf.py`) labels "GFLOPS". Read 2026-10.
- Meta AI Research (FAIR), *DINOv2* README ([GitHub, main branch](https://github.com/facebookresearch/dinov2/blob/main/README.md)): code and weights under the Apache License 2.0; XRay-DINO and Cell-DINO weights under the FAIR Noncommercial Research License. Read 2026-10.
- OpenAI, *CLIP* README and model card ([README](https://github.com/openai/CLIP/blob/main/README.md), [model card](https://github.com/openai/CLIP/blob/main/model-card.md), GitHub, main branch): zero-shot ImageNet performance matching the original ResNet-50; deployed use out of scope. Read 2026-10.
- Hendrycks and Dietterich, *robustness* README ([GitHub, master branch](https://github.com/hendrycks/robustness/blob/master/README.md)): ImageNet-C's 15 corruptions and ImageNet-A. Read 2026-10.
- COCO API source, `PythonAPI/pycocotools/cocoeval.py` ([GitHub, master branch](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py)): IoU thresholds from 0.50 to 0.95 in steps of 0.05. Read 2026-10.
- PyTorch torchvision source, `torchvision/models/mobilenetv3.py` ([GitHub, main branch](https://github.com/pytorch/vision/blob/main/torchvision/models/mobilenetv3.py)): MobileNetV3-Large lists `_ops` of 0.217, labelled "GFLOPS" in torchvision's `docs/source/conf.py`. Read 2026-10.
- TensorFlow Models, *MobileNet* README ([GitHub, master branch](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/README.md)): MobileNetV3-Large latency and accuracy, float and 8-bit, on a Pixel 1; 217 million MACs for MobileNetV3-Large in its checkpoint table ("Large dm=1 (float)"). Read 2026-10.
- The two illustrations are invented. Their numbers come from the worked examples in lessons 1 and 7.
