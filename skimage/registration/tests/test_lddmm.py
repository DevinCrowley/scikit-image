import pytest
from itertools import product
import numpy as np

from scipy.ndimage import rotate
from scipy.ndimage import map_coordinates

from skimage.registration import _lddmm_utilities

from skimage.registration._lddmm import lddmm_register

"""
Test lddmm_register.
"""


class Test_lddmm_register:
    def _test_lddmm_register(
        self, rtol=0, atol=1 - 1e-9, **lddmm_register_kwargs
    ):
        """
        A helper method for this class to verify registrations once they are
        computed.
        """

        lddmm_output = lddmm_register(**lddmm_register_kwargs)

        reference_image = lddmm_register_kwargs["reference_image"].astype(
            float
        )
        moving_image = lddmm_register_kwargs["moving_image"].astype(float)
        reference_image_spacing = (
            lddmm_register_kwargs["reference_image_spacing"]
            if "reference_image_spacing" in lddmm_register_kwargs.keys()
            else 1
        )
        moving_image_spacing = (
            lddmm_register_kwargs["moving_image_spacing"]
            if "moving_image_spacing" in lddmm_register_kwargs.keys()
            else 1
        )

        # Applying the transforms using map_coordinates assumes
        # map_coordinates_ify was left as True.

        deformed_moving_image = map_coordinates(
            input=moving_image,
            coordinates=lddmm_output.moving_image_to_reference_image_transform,
        )

        deformed_reference_image = map_coordinates(
            input=reference_image,
            coordinates=lddmm_output.reference_image_to_moving_image_transform,
        )

        assert np.allclose(
            deformed_reference_image, moving_image, rtol=rtol, atol=atol
        )
        assert np.allclose(
            deformed_moving_image, reference_image, rtol=rtol, atol=atol
        )

    def test_2D_identity_registration(self):

        ndims = 2
        radius = 3
        zero_space = 2
        center_pixel = True
        reference_image = np.zeros(
            tuple([(radius + zero_space) * 2 + center_pixel] * ndims)
        )
        for indices in product(*map(range, reference_image.shape)):
            indices = np.array(indices)
            if (
                np.sqrt(
                    np.sum(
                        (
                            indices
                            - (radius + zero_space)
                            + (not center_pixel) / 2
                        )
                        ** 2
                    )
                )
                <= radius
            ):
                reference_image[tuple(indices)] = 1
        moving_image = np.copy(reference_image)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=1,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_3D_identity_registration(self):

        ndims = 3
        radius = 3
        zero_space = 2
        center_pixel = True
        reference_image = np.zeros(
            tuple([(radius + zero_space) * 2 + center_pixel] * ndims)
        )
        for indices in product(*map(range, reference_image.shape)):
            indices = np.array(indices)
            if (
                np.sqrt(
                    np.sum(
                        (
                            indices
                            - (radius + zero_space)
                            + (not center_pixel) / 2
                        )
                        ** 2
                    )
                )
                <= radius
            ):
                reference_image[tuple(indices)] = 1
        moving_image = np.copy(reference_image)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=1,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_4D_identity_registration(self):

        ndims = 4
        radius = 3
        zero_space = 2
        center_pixel = True
        reference_image = np.zeros(
            tuple([(radius + zero_space) * 2 + center_pixel] * ndims)
        )
        for indices in product(*map(range, reference_image.shape)):
            indices = np.array(indices)
            if (
                np.sqrt(
                    np.sum(
                        (
                            indices
                            - (radius + zero_space)
                            + (not center_pixel) / 2
                        )
                        ** 2
                    )
                )
                <= radius
            ):
                reference_image[tuple(indices)] = 1
        moving_image = np.copy(reference_image)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=1,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_identity_disk_to_disk_registration(self):

        reference_image = np.array(
            [
                [(col - 4) ** 2 + (row - 4) ** 2 <= 4 ** 2 for col in range(9)]
                for row in range(9)
            ],
            int,
        )
        moving_image = np.copy(reference_image)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_affine_only_iterations=0,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_rigid_affine_only_ellipsoid_to_ellipsoid_registration(self):

        # reference_image (before padding) has shape (21, 29)
        # and semi-radii 4 and 10.
        reference_image = np.array(
            [
                [
                    (col - 14) ** 2 / 10 ** 2 + (row - 8) ** 2 / 4 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(17)
            ],
            int,
        )
        # templata and moving_image are opposite rotations of an unrotated
        # ellipsoid for symmetry.
        moving_image = rotate(reference_image, 45 / 2)
        reference_image = rotate(reference_image, -45 / 2)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=50,
            num_affine_only_iterations=50,
            num_rigid_affine_iterations=50,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_non_rigid_affine_only_ellipsoid_to_ellipsoid_registration(self):

        # reference_image (before padding) has shape (21, 29)
        # and semi-radii 6 and 10.
        reference_image = np.array(
            [
                [
                    (col - 14) ** 2 / 10 ** 2 + (row - 10) ** 2 / 6 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(21)
            ],
            int,
        )
        # moving_image is a rotation of reference_image.
        moving_image = rotate(reference_image, 30)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=50,
            num_affine_only_iterations=50,
            num_rigid_affine_iterations=0,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_partially_rigid_affine_only_ellipsoid_to_ellipsoid_registration(
        self,
    ):

        # reference_image (before padding) has shape (21, 29)
        # and semi-radii 6 and 10.
        reference_image = np.array(
            [
                [
                    (col - 14) ** 2 / 10 ** 2 + (row - 10) ** 2 / 6 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(21)
            ],
            int,
        )
        # moving_image is a rotation of reference_image.
        moving_image = rotate(reference_image, 30)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=100,
            num_affine_only_iterations=100,
            num_rigid_affine_iterations=50,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_deformative_only_disk_to_ellipsoid_registration(self):

        # reference_image has shape (25, 25) and radius 8.
        reference_image = np.array(
            [
                [
                    (col - 12) ** 2 + (row - 12) ** 2 <= 8 ** 2
                    for col in range(25)
                ]
                for row in range(25)
            ],
            int,
        )
        # moving_image has shape (21, 29) and semi-radii 6 and 10.
        moving_image = np.array(
            [
                [
                    (col - 14) ** 2 / 10 ** 2 + (row - 10) ** 2 / 6 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(21)
            ],
            int,
        )

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=150,
            num_affine_only_iterations=0,
            affine_stepsize=0,
            deformative_stepsize=0.5,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_general_ellipsoid_to_ellipsoid_registration(self):

        # moving_image has shape (21, 29) and semi-radii 6 and 10.
        reference_image = np.array(
            [
                [
                    (col - 14) ** 2 / 10 ** 2 + (row - 10) ** 2 / 6 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(21)
            ],
            int,
        )
        # moving_image has shape (21, 29) and semi-radii 6 and 10.
        moving_image = rotate(reference_image, 30)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            deformative_stepsize=0.5,
        )

        self._test_lddmm_register(**lddmm_register_kwargs)

    def test_identity_multiscale_registration(self):

        # moving_image has shape (21, 29) and semi-radii 6 and 10.
        reference_image = np.array(
            [
                [
                    (col - 14) ** 2 / 12 ** 2 + (row - 10) ** 2 / 8 ** 2 <= 1
                    for col in range(29)
                ]
                for row in range(21)
            ],
            int,
        )
        moving_image = np.copy(reference_image)

        lddmm_register_kwargs = dict(
            reference_image=reference_image,
            moving_image=moving_image,
            num_iterations=1,
            multiscales=[5, (2, 3), [3, 2], 1],
        )

        self._test_lddmm_register(**lddmm_register_kwargs)


if __name__ == "__main__":
    test_lddmm_register()
