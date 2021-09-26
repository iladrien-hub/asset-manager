import bpy

RAD = 0.01745333333

# Прозрачный фон
bpy.context.scene.render.film_transparent = True

camera = bpy.data.objects['Camera']
bpy.context.scene.camera = camera

camera_origin = bpy.data.objects['Camera_origin']

x_origin = bpy.data.objects['X_origin']
y_origin = bpy.data.objects['Y_origin']
z_origin = bpy.data.objects['Z_origin']

print(camera)

iterations = 20
step = 360 / iterations

for i in range(iterations):
    x_origin.rotation_euler[2] = (45 + step * i) * RAD
    y_origin.rotation_euler[2] = (45 + step * i) * RAD
    z_origin.rotation_euler[2] = (45 + step * i) * RAD

    camera_origin.rotation_euler[2] = step * i * RAD
    bpy.context.scene.render.filepath = f"E:\\Projects\\.minectaft\\admin\\backend\\resources\\visualizer\\sideways_spinset\\{i}.png"
    bpy.ops.render.render(write_still=True)