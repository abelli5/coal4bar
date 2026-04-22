"""Test suite for coal4bar module"""

import unittest
import math
import numpy as np
import sys
sys.path.insert(0, '..')

from coal4bar.structure import FourBarLinkage, FourBarDimensions
from coal4bar.forces import ForceAnalysis
from coal4bar.safety_analysis import SafetyAnalyzer


class TestFourBarLinkage(unittest.TestCase):
    """Test cases for FourBarLinkage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = FourBarDimensions(
            base_length=1000,
            input_crank=250,
            coupler=800,
            output_link=600
        )
        self.linkage = FourBarLinkage(self.dimensions)
    
    def test_grashof_criterion(self):
        """Test Grashof criterion validation."""
        self.assertTrue(self.dimensions.validate_grashof_criterion())
    
    def test_forward_kinematics(self):
        """Test forward kinematics calculation."""
        angle = math.radians(45)
        C, D = self.linkage.forward_kinematics(angle)
        
        # Check that joint positions are returned
        self.assertIsNotNone(C)
        self.assertIsNotNone(D)
        self.assertEqual(len(C), 2)
        self.assertEqual(len(D), 2)
    
    def test_link_length_preservation(self):
        """Test that link lengths are preserved during kinematics."""
        angle = math.radians(60)
        self.linkage.forward_kinematics(angle)
        
        positions = self.linkage.get_joint_positions()
        
        # Check each link length
        AC_length = np.linalg.norm(positions['C'] - positions['A'])
        self.assertAlmostEqual(AC_length, self.dimensions.input_crank, places=1)
        
        CD_length = np.linalg.norm(positions['D'] - positions['C'])
        self.assertAlmostEqual(CD_length, self.dimensions.coupler, places=1)
        
        BD_length = np.linalg.norm(positions['D'] - positions['B'])
        self.assertAlmostEqual(BD_length, self.dimensions.output_link, places=1)
    
    def test_output_angle_calculation(self):
        """Test output link angle calculation."""
        angle = math.radians(45)
        self.linkage.forward_kinematics(angle)
        
        output_angle = self.linkage.get_output_angle()
        
        # Output angle should be a valid number
        self.assertTrue(np.isfinite(output_angle))
    
    def test_multiple_angles(self):
        """Test kinematics at multiple input angles."""
        for angle_deg in range(30, 150, 15):
            angle = math.radians(angle_deg)
            with self.subTest(angle=angle_deg):
                C, D = self.linkage.forward_kinematics(angle)
                
                # All coordinates should be finite
                self.assertTrue(np.all(np.isfinite(C)))
                self.assertTrue(np.all(np.isfinite(D)))


class TestForceAnalysis(unittest.TestCase):
    """Test cases for ForceAnalysis class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = FourBarDimensions(
            base_length=1000,
            input_crank=250,
            coupler=800,
            output_link=600
        )
        self.linkage = FourBarLinkage(self.dimensions)
        self.analyzer = ForceAnalysis(self.linkage)
    
    def test_force_analysis_basic(self):
        """Test basic force analysis."""
        self.linkage.forward_kinematics(math.radians(45))
        
        result = self.analyzer.analyze_static_forces(coal_force=50000)
        
        # Check result structure
        self.assertIn('coal_force', result)
        self.assertIn('hydraulic_force', result)
        self.assertIn('mechanical_advantage', result)
        self.assertIn('bearing_loads', result)
    
    def test_mechanical_advantage_positive(self):
        """Test that mechanical advantage is positive."""
        self.linkage.forward_kinematics(math.radians(45))
        
        result = self.analyzer.analyze_static_forces(coal_force=50000)
        
        self.assertGreater(result['mechanical_advantage'], 0)
    
    def test_bearing_loads_non_negative(self):
        """Test that bearing loads are non-negative."""
        self.linkage.forward_kinematics(math.radians(45))
        
        result = self.analyzer.analyze_static_forces(coal_force=50000)
        
        for joint in ['A', 'B', 'C', 'D']:
            self.assertGreaterEqual(result['bearing_loads'][joint], 0)


class TestSafetyAnalyzer(unittest.TestCase):
    """Test cases for SafetyAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dimensions = FourBarDimensions(
            base_length=1000,
            input_crank=250,
            coupler=800,
            output_link=600
        )
        self.linkage = FourBarLinkage(self.dimensions)
        self.analyzer = SafetyAnalyzer(self.linkage)
    
    def test_stability_analysis(self):
        """Test linkage stability analysis."""
        stability = self.analyzer.analyze_linkage_stability()
        
        self.assertIn('is_grashof_mechanism', stability)
        self.assertIn('aspect_ratios', stability)
        self.assertIn('linkage_type', stability)
    
    def test_safety_factor_calculation(self):
        """Test safety factor calculations."""
        stress = 100e6  # 100 MPa
        sf = self.analyzer.calculate_static_safety_factor(stress)
        
        # Should be reasonable (material is 345 MPa yield)
        self.assertGreater(sf, 1)
        self.assertLess(sf, 10)
    
    def test_zero_stress_infinite_sf(self):
        """Test that zero stress gives infinite safety factor."""
        sf = self.analyzer.calculate_static_safety_factor(0)
        
        self.assertEqual(sf, float('inf'))
    
    def test_bearing_analysis(self):
        """Test bearing safety analysis."""
        bearing_analysis = self.analyzer.analyze_bearing_loads(50000)
        
        self.assertIn('contact_pressure', bearing_analysis)
        self.assertIn('safety_factor_bearing', bearing_analysis)
        self.assertIn('L10_life_hours', bearing_analysis)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow."""
    
    def test_complete_analysis_workflow(self):
        """Test complete analysis from linkage to safety."""
        # Create linkage
        dimensions = FourBarDimensions(
            base_length=1000,
            input_crank=250,
            coupler=800,
            output_link=600
        )
        linkage = FourBarLinkage(dimensions)
        
        # Forward kinematics
        linkage.forward_kinematics(math.radians(45))
        
        # Force analysis
        force_analyzer = ForceAnalysis(linkage)
        forces = force_analyzer.analyze_static_forces(coal_force=50000)
        
        # Safety analysis
        safety_analyzer = SafetyAnalyzer(linkage)
        stability = safety_analyzer.analyze_linkage_stability()
        
        # All should complete without errors
        self.assertIsNotNone(linkage.D)
        self.assertGreater(forces['mechanical_advantage'], 0)
        self.assertTrue(stability['is_grashof_mechanism'])


if __name__ == '__main__':
    unittest.main()
