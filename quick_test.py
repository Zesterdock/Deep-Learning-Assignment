"""
Quick Video Test - Process sample frames from each video
"""
import cv2
from bag_counter import process_video
import time

def quick_test_video(video_path, scenario_name, max_frames=500):
    """Test a video with limited frames for quick results"""
    print(f"\n{'='*60}")
    print(f"Testing: {scenario_name}")
    print(f"Video: {video_path}")
    print(f"{'='*60}")
    
    start_time = time.time()
    frame_count = 0
    final_bags_in = 0
    final_bags_out = 0
    
    try:
        for frame, bags_in, bags_out in process_video(video_path):
            frame_count += 1
            final_bags_in = bags_in
            final_bags_out = bags_out
            
            # Show progress every 100 frames
            if frame_count % 100 == 0:
                print(f"  Frame {frame_count}: Bags In={bags_in}, Bags Out={bags_out}")
            
            # Stop after max_frames for quick testing
            if frame_count >= max_frames:
                print(f"\n  Processed {max_frames} frames (quick test mode)")
                break
        
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\n✅ {scenario_name} - COMPLETED")
        print(f"  Frames Processed: {frame_count}")
        print(f"  Bags In (Loading): {final_bags_in}")
        print(f"  Bags Out (Unloading): {final_bags_out}")
        print(f"  Total Bags: {final_bags_in + final_bags_out}")
        print(f"  Processing Time: {elapsed_time:.2f}s")
        print(f"  Average FPS: {fps:.2f}")
        
        return {
            'scenario': scenario_name,
            'success': True,
            'frames': frame_count,
            'bags_in': final_bags_in,
            'bags_out': final_bags_out,
            'total': final_bags_in + final_bags_out,
            'time': elapsed_time,
            'fps': fps
        }
        
    except Exception as e:
        print(f"\n❌ {scenario_name} - ERROR")
        print(f"  Error: {str(e)}")
        return {
            'scenario': scenario_name,
            'success': False,
            'error': str(e)
        }

def main():
    """Quick test on all 3 scenarios"""
    print("\n" + "="*60)
    print("BAG COUNTER - QUICK MULTI-VIDEO TEST")
    print("="*60)
    print("Processing 500 frames per video for quick results...")
    
    videos = [
        ("input/Problem Statement Scenario1.mp4", "Scenario 1"),
        ("input/Problem Statement Scenario2.mp4", "Scenario 2"),
        ("input/Problem Statement Scenario3.mp4", "Scenario 3"),
    ]
    
    results = []
    
    for video_path, scenario_name in videos:
        result = quick_test_video(video_path, scenario_name, max_frames=500)
        results.append(result)
        time.sleep(0.5)
    
    # Summary Report
    print("\n" + "="*60)
    print("QUICK TEST SUMMARY")
    print("="*60)
    
    total_bags = 0
    successful_tests = 0
    
    for result in results:
        if result['success']:
            successful_tests += 1
            total_bags += result['total']
            print(f"\n{result['scenario']}:")
            print(f"  ✅ Status: PASSED")
            print(f"  📊 Bags In: {result['bags_in']}")
            print(f"  📊 Bags Out: {result['bags_out']}")
            print(f"  📊 Total: {result['total']}")
            print(f"  ⚡ FPS: {result['fps']:.2f}")
        else:
            print(f"\n{result['scenario']}:")
            print(f"  ❌ Status: FAILED")
            print(f"  Error: {result.get('error', 'Unknown')}")
    
    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"  Tests Passed: {successful_tests}/3")
    print(f"  Total Bags Counted: {total_bags}")
    print(f"\n  Note: This is a quick test (500 frames per video)")
    print(f"  For complete results, run: python test_all_videos.py")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
