import random
from subprocess import call

import torch
import skimage
import skimage.io
import click
import ttools.modules

import pydiffvg

pydiffvg.set_print_timing(True)

gamma = 1.0

@click.command()
@click.argument(
    'target_image',
)
@click.option(
    '--num_paths',
    type=int,
    default=512,
    show_default=True,
)
@click.option(
    '--max_width',
    type=float,
    default=2.0,
    show_default=True,
)
@click.option(
    '--method',
    type=click.Choice(['lpips', 'blob'], case_sensitive=False),
    default='lpips',
    show_default=True,
)
@click.option(
    '--iters',
    type=int,
    default=500,
    show_default=True,
)
@click.option(
    '--background_color',
    help='RGB for backgound color range between 0 and 255 for each value. If None specified white is used.',
    type=int,
    nargs=3,
)
@click.option(
    '--seed',
    help='Seed used for random values.',
    type=int,
    default=1234,
    show_default=True,
)
def image_to_svg(
    target_image,
    num_paths,
    max_width,
    method,
    iters,
    background_color,
    seed,
):

    pydiffvg.set_use_gpu(torch.cuda.is_available())
    
    perception_loss = ttools.modules.LPIPS().to(pydiffvg.get_device())
    
    target = torch.from_numpy(skimage.io.imread(target_image)).to(torch.float32) / 255.0
    target = target.pow(gamma)
    target = target.to(pydiffvg.get_device())
    target = target.unsqueeze(0)
    target = target.permute(0, 3, 1, 2) # NHWC -> NCHW

    canvas_width, canvas_height = target.shape[3], target.shape[2]
    
    random.seed(seed)
    torch.manual_seed(seed)

    background_image = None
    target_background_image = None
    if len(background_color) == 3:
      background_image = torch.zeros((canvas_height, canvas_width, 3), dtype=torch.float32)
      background_image[:, :, 0] = background_color[0] / 255.0
      background_image[:, :, 1] = background_color[1] / 255.0
      background_image[:, :, 2] = background_color[2] / 255.0
      # background_image = torch.tensor(background_image)

      target_background_image = torch.zeros((target.shape[0], target.shape[1], 3), dtype=torch.float32)
      target_background_image[:, :, 0] = background_color[0] / 255.0
      target_background_image[:, :, 1] = background_color[1] / 255.0
      target_background_image[:, :, 2] = background_color[2] / 255.0

    
    shapes = []
    shape_groups = []
    if method == 'blob':
        for i in range(num_paths):
            num_segments = random.randint(3, 5)
            num_control_points = torch.zeros(num_segments, dtype = torch.int32) + 2
            points = []
            p0 = (random.random(), random.random())
            points.append(p0)
            for j in range(num_segments):
                radius = 0.05
                p1 = (p0[0] + radius * (random.random() - 0.5), p0[1] + radius * (random.random() - 0.5))
                p2 = (p1[0] + radius * (random.random() - 0.5), p1[1] + radius * (random.random() - 0.5))
                p3 = (p2[0] + radius * (random.random() - 0.5), p2[1] + radius * (random.random() - 0.5))
                points.append(p1)
                points.append(p2)
                if j < num_segments - 1:
                    points.append(p3)
                    p0 = p3
            points = torch.tensor(points)
            points[:, 0] *= canvas_width
            points[:, 1] *= canvas_height
            path = pydiffvg.Path(num_control_points = num_control_points,
                                 points = points,
                                 stroke_width = torch.tensor(1.0),
                                 is_closed = True)
            shapes.append(path)
            path_group = pydiffvg.ShapeGroup(shape_ids = torch.tensor([len(shapes) - 1]),
                                             fill_color = torch.tensor([random.random(),
                                                                        random.random(),
                                                                        random.random(),
                                                                        random.random()]))
            shape_groups.append(path_group)
    else:
        for i in range(num_paths):
            num_segments = random.randint(1, 3)
            num_control_points = torch.zeros(num_segments, dtype = torch.int32) + 2
            points = []
            p0 = (random.random(), random.random())
            points.append(p0)
            for j in range(num_segments):
                radius = 0.05
                p1 = (p0[0] + radius * (random.random() - 0.5), p0[1] + radius * (random.random() - 0.5))
                p2 = (p1[0] + radius * (random.random() - 0.5), p1[1] + radius * (random.random() - 0.5))
                p3 = (p2[0] + radius * (random.random() - 0.5), p2[1] + radius * (random.random() - 0.5))
                points.append(p1)
                points.append(p2)
                points.append(p3)
                p0 = p3
            points = torch.tensor(points)
            points[:, 0] *= canvas_width
            points[:, 1] *= canvas_height

            path = pydiffvg.Path(num_control_points = num_control_points,
                                 points = points,
                                 stroke_width = torch.tensor(1.0),
                                 is_closed = False)
            shapes.append(path)
            path_group = pydiffvg.ShapeGroup(shape_ids = torch.tensor([len(shapes) - 1]),
                                             fill_color = None,
                                             stroke_color = torch.tensor([random.random(),
                                                                          random.random(),
                                                                          random.random(),
                                                                          random.random()]))
            shape_groups.append(path_group)
    
    scene_args = pydiffvg.RenderFunction.serialize_scene(\
        canvas_width, canvas_height, shapes, shape_groups)
    
    render = pydiffvg.RenderFunction.apply
    img = render(canvas_width, # width
                 canvas_height, # height
                 2,   # num_samples_x
                 2,   # num_samples_y
                 seed,   # seed
                 background_image,
                 *scene_args)
    pydiffvg.imwrite(img.cpu(), 'results/painterly_rendering/init.png', gamma=gamma)

    points_vars = []
    stroke_width_vars = []
    color_vars = []
    for path in shapes:
        path.points.requires_grad = True
        points_vars.append(path.points)
    if method == 'lpips':
        for path in shapes:
            path.stroke_width.requires_grad = True
            stroke_width_vars.append(path.stroke_width)

    if method == 'blob':
        for group in shape_groups:
            group.fill_color.requires_grad = True
            color_vars.append(group.fill_color)
    else:
        for group in shape_groups:
            group.stroke_color.requires_grad = True
            color_vars.append(group.stroke_color)
    
    # Optimize
    points_optim = torch.optim.Adam(points_vars, lr=1.0)
    if len(stroke_width_vars) > 0:
        width_optim = torch.optim.Adam(stroke_width_vars, lr=0.1)
    color_optim = torch.optim.Adam(color_vars, lr=0.01)
    # Adam iterations.
    for t in range(iters):
        print('iteration:', t)
        points_optim.zero_grad()
        if len(stroke_width_vars) > 0:
            width_optim.zero_grad()
        color_optim.zero_grad()
        # Forward pass: render the image.
        scene_args = pydiffvg.RenderFunction.serialize_scene(\
            canvas_width, canvas_height, shapes, shape_groups)
        img = render(canvas_width, # width
                     canvas_height, # height
                     2,   # num_samples_x
                     2,   # num_samples_y
                     seed + t,   # seed
                     background_image,
                     *scene_args)
        # Compose img with white background
        img = img[:, :, 3:4] * img[:, :, :3] + torch.ones(img.shape[0], img.shape[1], 3, device = pydiffvg.get_device()) * (1 - img[:, :, 3:4])
        # Save the intermediate render.
        pydiffvg.imwrite(img.cpu(), 'results/painterly_rendering/iter_{}.png'.format(t), gamma=gamma)
        img = img[:, :, :3]
        # Convert img from HWC to NCHW
        img = img.unsqueeze(0)
        img = img.permute(0, 3, 1, 2) # NHWC -> NCHW
        if method == 'lpips':
            loss = perception_loss(img, target) + (img.mean() - target.mean()).pow(2)
        else:
            loss = (img - target).pow(2).mean()
        print('render loss:', loss.item())
    
        # Backpropagate the gradients.
        loss.backward()

        # Take a gradient descent step.
        points_optim.step()
        if len(stroke_width_vars) > 0:
            width_optim.step()
        color_optim.step()
        if len(stroke_width_vars) > 0:
            for path in shapes:
                path.stroke_width.data.clamp_(1.0, max_width)
        if method == 'blob':
            for group in shape_groups:
                group.fill_color.data.clamp_(0.0, 1.0)
        else:
            for group in shape_groups:
                group.stroke_color.data.clamp_(0.0, 1.0)

        if t % 10 == 0 or t == iters - 1:
            pydiffvg.save_svg('results/painterly_rendering/iter_{}.svg'.format(t),
                              canvas_width, canvas_height, shapes, shape_groups)
    
    img = render(target.shape[1], # width
                 target.shape[0], # height
                 2,   # num_samples_x
                 2,   # num_samples_y
                 seed,   # seed
                 target_background_image,
                 *scene_args)
    
    # Save the intermediate render.
    pydiffvg.imwrite(img.cpu(), 'results/painterly_rendering/final.png'.format(t), gamma=gamma)
    # Convert the intermediate renderings to a video.
    call(["ffmpeg", "-framerate", "24", "-i",
        "results/painterly_rendering/iter_%d.png", "-vb", "20M", "-vcodec", "libx264", "-crf", "25", "-pix_fmt", "yuv420p",
        "results/painterly_rendering/out.mp4"])
    

if __name__ == "__main__":
    painterly_rendering()
