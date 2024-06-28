<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Cropper from 'svelte-easy-crop';
	import { updateProfile } from '$lib/users_api';

	export let showModal: boolean;
	export let firstName: string;
	export let lastName: string;
	export let userId: number;

	let newFirstName = firstName;
	let newLastName = lastName;
	let profilePicture: File | null = null;
	let croppedImage: string | null = null;
	let showCropper = false;
	let crop = { x: 0, y: 0 };
	let zoom = 1;
	let aspect = 1;
	let croppedAreaPixels: any = null;

	const dispatch = createEventDispatcher();

	function closeModal() {
		dispatch('close');
	}

	async function handleSubmit() {
		const profileData: { first_name: string, last_name: string, profile_picture?: string | null } = {
			first_name: newFirstName,
			last_name: newLastName,
			profile_picture: ''
		};

		console.log('Cropped image:', croppedImage)
		if (croppedImage) {
			profileData.profile_picture = croppedImage.split(',')[1];
		}

		try {
			console.log('Updating profile:', profileData);
			await updateProfile(userId, profileData);
			closeModal();
			// window.location.reload();
		} catch (error) {
			console.error('Failed to update profile:', error);
			alert('Failed to update profile. Please try again.');
		}
	}

	function handleFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.files && target.files[0]) {
			profilePicture = target.files[0];
			showCropper = true;
			croppedImage = null;
		}
	}

	function handleCropComplete(event: CustomEvent) {
		croppedAreaPixels = event.detail;
	}


async function handleCropConfirm() {
    console.log('Confirming crop');
    console.log('profilePicture:', profilePicture);
    console.log('croppedAreaPixels:', croppedAreaPixels);

    if (profilePicture && croppedAreaPixels) {
        try {
            const imageUrl = URL.createObjectURL(profilePicture);
            console.log('Image URL created:', imageUrl);

            const croppedImageResult = await getCroppedImg(imageUrl, croppedAreaPixels.pixels);
            console.log('Cropped image result:', croppedImageResult ? 'success' : 'null');

            if (croppedImageResult) {
                croppedImage = croppedImageResult;
                console.log('Cropped image set:', croppedImage.substring(0, 50) + '...');
            } else {
                console.error('Failed to get cropped image');
            }
            showCropper = false;
        } catch (error) {
            console.error('Error cropping image:', error);
        }
    } else {
        console.log('Unable to crop: profilePicture or croppedAreaPixels is null');
        if (!profilePicture) console.log('profilePicture is null');
        if (!croppedAreaPixels) console.log('croppedAreaPixels is null');
    }
}

async function getCroppedImg(imageSrc: string, pixelCrop: any): Promise<string | null> {
    console.log('Getting cropped image');
    console.log('Image source:', imageSrc);
    console.log('Pixel crop:', pixelCrop);

    try {
        const image = await createImage(imageSrc);
        console.log('Image created successfully');

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        if (!ctx) {
            console.error('Unable to get 2D context');
            return null;
        }

        canvas.width = pixelCrop.width;
        canvas.height = pixelCrop.height;

        ctx.drawImage(
            image,
            pixelCrop.x,
            pixelCrop.y,
            pixelCrop.width,
            pixelCrop.height,
            0,
            0,
            pixelCrop.width,
            pixelCrop.height
        );

        const imageData = canvas.toDataURL('image/jpeg', 0.95);
        console.log('Image data URL created:', imageData.substring(0, 50) + '...');

        return imageData;
    } catch (error) {
        console.error('Error in getCroppedImg:', error);
        return null;
    }
}

function createImage(url: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
        const image = new Image();
        image.addEventListener('load', () => {
            console.log('Image loaded successfully');
            resolve(image);
        });
        image.addEventListener('error', (error) => {
            console.error('Error loading image:', error);
            reject(error);
        });
        image.src = url;
    });
}
</script>

{#if showModal}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center modal">
		<div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
			<h2 class="text-2xl mb-4">Edit Profile</h2>
			<form on:submit|preventDefault={handleSubmit}>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="firstname">First Name</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="firstname"
						type="text"
						placeholder="First Name"
						bind:value={newFirstName}
						required
					>
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="lastname">Last Name</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="lastname"
						type="text"
						placeholder="Last Name"
						bind:value={newLastName}
						required
					>
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="profilePicture">Profile
						Picture</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="profilePicture"
						type="file"
						accept="image/*"
						on:change={handleFileChange}
					>
				</div>
				{#if showCropper && profilePicture}
					<div class="mb-4">
						<p class="text-sm text-gray-600 mb-2">Adjust the image and click 'Confirm Crop' when ready.</p>
						<div class="h-64 relative">
							<Cropper
								image={URL.createObjectURL(profilePicture)}
								bind:crop
								bind:zoom
								aspect={aspect}
								on:cropcomplete={handleCropComplete}
							/>
						</div>
						<button type="button" class="btn bg-green-500 hover:bg-green-600 text-white mt-4 w-full"
								on:click={handleCropConfirm}>
							Confirm Crop
						</button>
					</div>
				{:else if croppedImage}
					<div class="mb-4">
						<p class="text-sm text-gray-600 mb-2">Cropped Image Preview:</p>
						<img src={croppedImage} alt="" aria-hidden="true"
							 class="w-32 h-32 object-cover mx-auto">
					</div>
				{/if}
				<div class="flex items-center justify-between mt-6">
					<button class="btn bg-indigo-custom" type="submit">Save Changes</button>
					<button class="btn bg-gray-600 hover:bg-gray-700 rounded-md text-white" type="button"
							on:click={closeModal}>
						Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<style lang="postcss">
    .modal {
        z-index: 3;
    }

    .btn {
        @apply font-bold py-2 px-4 rounded;
    }

    .btn.bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white;
    }
</style>
